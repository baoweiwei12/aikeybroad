import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, conint
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail
import asyncio
import json
from fastapi import (
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)

from app.service.streaming_asr import AsrWsClient, AudioType, read_wav_info


router = APIRouter(prefix="", tags=["speech_to_text"])


@router.websocket("/speech_to_text")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_bytes()
            if not data:
                logging.error("Received empty data")
                await websocket.send_text(json.dumps({"error": "Received empty data"}))
                continue

            # 需要至少1KB大小
            if len(data) < 1024:
                logging.error("Received data is too short to be valid audio")
                await websocket.send_text(
                    json.dumps(
                        {"error": "Received data is too short to be valid audio"}
                    )
                )
                continue

            # 使用传入的音频数据
            audio_data = data

            # 将音频数据传递给 AsrWsClient 进行处理
            asr_client = AsrWsClient(
                audio_path=None,
                cluster="volcengine_streaming_common",
                appid="4842826137",
                token="taUewQocVhMqs1pkbjl7zuDQSR-YxMR1",
                format="mp3",
                audio_type=AudioType.LOCAL,
            )

            try:
                # 处理音频数据
                if asr_client.format == "mp3":
                    segment_size = asr_client.mp3_seg_size
                    result = await asr_client.segment_data_processor(
                        audio_data, segment_size
                    )
                else:
                    nchannels, sampwidth, framerate, nframes, wav_len = read_wav_info(
                        audio_data
                    )
                    size_per_sec = nchannels * sampwidth * framerate
                    segment_size = int(size_per_sec * asr_client.seg_duration / 1000)
                    result = await asr_client.segment_data_processor(
                        audio_data, segment_size
                    )
            except asyncio.TimeoutError:
                logging.error("Connection timed out while processing audio data")
                await websocket.send_text(
                    json.dumps(
                        {"error": "Connection timed out while processing audio data"}
                    )
                )
                continue
            except WebSocketException as e:
                logging.error(f"WebSocket error: {e}")
                await websocket.send_text(
                    json.dumps({"error": f"WebSocket error: {e}"})
                )
                continue
            except Exception as e:
                logging.error(f"Error processing audio data: {e}")
                await websocket.send_text(
                    json.dumps({"error": f"Error processing audio data: {e}"})
                )
                continue

            # 将处理结果发送回客户端
            await websocket.send_text(json.dumps(result))
    except WebSocketDisconnect:
        logging.info("WebSocket connection was closed")
