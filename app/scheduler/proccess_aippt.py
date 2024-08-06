import logging
from app import schemas
from app.core.database import SessionLocal
from app.crud import aippt, api_config
from app.service.xunfei_aippt import XunFeiAiPPTClient
def proccess_aippt():
    try:
        db = SessionLocal()

        config = api_config.random_get_enabled_api_config_xunfei_ai_ppt(db)
        if config is None:
            logging.info("No enabled api config")
            return
        client = XunFeiAiPPTClient(config.app_id, config.api_secret)  # type: ignore
        unfinished_task = aippt.get_unfinished_ai_ppt_record(db, max_errors=10)
        if unfinished_task is None:
            logging.info("No unfinished task")
            return
        try:
            unfinished_task_proccess = client.get_task_progress(unfinished_task.sid)  # type: ignore
            updated_task = aippt.update_ai_ppt_record(
                db,
                unfinished_task.sid,  # type: ignore
                schemas.AiPPTRecordUpdate(
                    process=unfinished_task_proccess.process,
                    ppt_url=unfinished_task_proccess.pptUrl,
                    err_msg=unfinished_task_proccess.errMsg,
                ),
            )
            if updated_task is None:
                logging.info(f"Not found updated task: {unfinished_task.sid}")
                return
            logging.info(f"Task proccessed sid:{updated_task.sid}")
        except Exception as e:
            logging.error(e)
            aippt.update_ai_ppt_record(
                db,
                unfinished_task.sid,  # type: ignore
                schemas.AiPPTRecordUpdate(
                    error_count=int(str(unfinished_task.error_count)) + 1,
                ),
            )
            return
    finally:
        db.close()