import argparse
import uvicorn
import os
import json
import base64
import secrets
import string
import yaml


def save_folder_to_py(folder_path: str = "app", output_py: str = "init.py"):
    """
    将文件夹中的所有文件和文件结构保存到一个 Python 脚本中。
    :param folder_path: 要保存的文件夹路径
    :param output_py: 保存输出的 Python 脚本路径
    """
    with open(output_py, "w", encoding="utf-8") as f:
        f.write("import os\nimport base64\n\n")
        f.write("def load_folder(target_folder: str):\n")

        for root, dirs, files in os.walk(folder_path):
            relative_path = os.path.relpath(root, folder_path)
            f.write(f"    # Creating directory: {relative_path}\n")
            f.write(
                f"    os.makedirs(os.path.join(target_folder, '{relative_path}'), exist_ok=True)\n\n"
            )

            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as file_content:
                    encoded_content = base64.b64encode(file_content.read()).decode(
                        "utf-8"
                    )
                    f.write(f"    # Writing file: {file}\n")
                    f.write(
                        f"    with open(os.path.join(target_folder, '{relative_path}', '{file}'), 'wb') as f:\n"
                    )
                    f.write(
                        f"        f.write(base64.b64decode({repr(encoded_content)}))\n\n"
                    )


def load_folder(target_folder: str = "app"):

    # Creating directory: .
    os.makedirs(os.path.join(target_folder, "."), exist_ok=True)

    # Writing file: main.py
    with open(os.path.join(target_folder, ".", "main.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "ZnJvbSBhcHAuY29yZS5jb25maWcgaW1wb3J0IENPTkZJRw0KZnJvbSBmYXN0YXBpIGltcG9ydCBGYXN0QVBJDQpmcm9tIGZhc3RhcGkubWlkZGxld2FyZS5jb3JzIGltcG9ydCBDT1JTTWlkZGxld2FyZQ0KZnJvbSBhcHAuYXBpIGltcG9ydCBhdXRoLCB1c2VyDQoNCmFwcCA9IEZhc3RBUEkoDQogICAgdGl0bGU9Q09ORklHLkFQUC5OQU1FLA0KICAgIGRlc2NyaXB0aW9uPUNPTkZJRy5BUFAuREVTQ1JJUFRJT04sDQogICAgdmVyc2lvbj1DT05GSUcuQVBQLlZFUlNJT04sDQopDQoNCmFwcC5hZGRfbWlkZGxld2FyZSgNCiAgICBDT1JTTWlkZGxld2FyZSwNCiAgICBhbGxvd19vcmlnaW5zPVsiKiJdLA0KICAgIGFsbG93X2NyZWRlbnRpYWxzPVRydWUsDQogICAgYWxsb3dfbWV0aG9kcz1bIioiXSwNCiAgICBhbGxvd19oZWFkZXJzPVsiKiJdLA0KKQ0KDQphcHAuaW5jbHVkZV9yb3V0ZXIoYXV0aC5yb3V0ZXIsIHByZWZpeD0iL2FwaSIpDQphcHAuaW5jbHVkZV9yb3V0ZXIodXNlci5yb3V0ZXIsIHByZWZpeD0iL2FwaSIpDQo="
            )
        )

    # Creating directory: api
    os.makedirs(os.path.join(target_folder, "api"), exist_ok=True)

    # Writing file: auth.py
    with open(os.path.join(target_folder, "api", "auth.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "ZnJvbSBmYXN0YXBpIGltcG9ydCBBUElSb3V0ZXIsIERlcGVuZHMsIEhUVFBFeGNlcHRpb24sIHN0YXR1cw0KZnJvbSBmYXN0YXBpLnNlY3VyaXR5IGltcG9ydCBPQXV0aDJQYXNzd29yZFJlcXVlc3RGb3JtDQpmcm9tIHB5ZGFudGljIGltcG9ydCBCYXNlTW9kZWwsIEVtYWlsU3RyDQpmcm9tIHNxbGFsY2hlbXkub3JtIGltcG9ydCBTZXNzaW9uDQpmcm9tIGFwcCBpbXBvcnQgY3J1ZCwgbW9kZWxzLCBzY2hlbWFzDQpmcm9tIGFwcC5jb3JlIGltcG9ydCBkZXBlbmRlbmNpZXMsIHNlY3VyaXR5DQoNCnJvdXRlciA9IEFQSVJvdXRlcihwcmVmaXg9IiIsIHRhZ3M9WyJhdXRoIl0pDQoNCg0KQHJvdXRlci5wb3N0KCIvbG9naW4vdG9rZW4iLCByZXNwb25zZV9tb2RlbD1zZWN1cml0eS5Ub2tlbikNCmRlZiBsb2dpbl9mb3JfYWNjZXNzX3Rva2VuKA0KICAgIGZvcm1fZGF0YTogT0F1dGgyUGFzc3dvcmRSZXF1ZXN0Rm9ybSA9IERlcGVuZHMoKSwNCiAgICBkYjogU2Vzc2lvbiA9IERlcGVuZHMoZGVwZW5kZW5jaWVzLmdldF9kYiksDQopOg0KICAgIHVzZXIgPSBjcnVkLmF1dGhlbnRpY2F0ZV91c2VyKGRiLCBmb3JtX2RhdGEudXNlcm5hbWUsIGZvcm1fZGF0YS5wYXNzd29yZCkNCiAgICBpZiBub3QgdXNlcjoNCiAgICAgICAgcmFpc2UgSFRUUEV4Y2VwdGlvbigNCiAgICAgICAgICAgIHN0YXR1c19jb2RlPXN0YXR1cy5IVFRQXzQwMV9VTkFVVEhPUklaRUQsDQogICAgICAgICAgICBkZXRhaWw9IkluY29ycmVjdCB1c2VybmFtZSBvciBwYXNzd29yZCIsDQogICAgICAgICAgICBoZWFkZXJzPXsiV1dXLUF1dGhlbnRpY2F0ZSI6ICJCZWFyZXIifSwNCiAgICAgICAgKQ0KICAgIGFjY2Vzc190b2tlbiA9IHNlY3VyaXR5LmNyZWF0ZV9hY2Nlc3NfdG9rZW4oZGF0YT17InN1YiI6IHVzZXIudXNlcm5hbWV9KQ0KICAgIHJldHVybiBzZWN1cml0eS5Ub2tlbihhY2Nlc3NfdG9rZW49YWNjZXNzX3Rva2VuLCB0b2tlbl90eXBlPSJiZWFyZXIiKQ0KDQoNCkByb3V0ZXIucG9zdCgiL3JlZnJlc2gvdG9rZW4iLCByZXNwb25zZV9tb2RlbD1zZWN1cml0eS5Ub2tlbikNCmRlZiByZWZyZXNoX2FjY2Vzc190b2tlbigNCiAgICBjdXJyZW50X3VzZXI6IG1vZGVscy5Vc2VyID0gRGVwZW5kcyhkZXBlbmRlbmNpZXMuZ2V0X2N1cnJlbnRfYWN0aXZlX3VzZXIpLA0KICAgIGRiOiBTZXNzaW9uID0gRGVwZW5kcyhkZXBlbmRlbmNpZXMuZ2V0X2RiKSwNCik6DQogICAgYWNjZXNzX3Rva2VuID0gc2VjdXJpdHkuY3JlYXRlX2FjY2Vzc190b2tlbihkYXRhPXsic3ViIjogY3VycmVudF91c2VyLnVzZXJuYW1lfSkNCiAgICByZXR1cm4gc2VjdXJpdHkuVG9rZW4oYWNjZXNzX3Rva2VuPWFjY2Vzc190b2tlbiwgdG9rZW5fdHlwZT0iYmVhcmVyIikNCg0KDQpjbGFzcyBVc2VyUmVnaXN0ZXIoQmFzZU1vZGVsKToNCiAgICB1c2VybmFtZTogc3RyDQogICAgZW1haWw6IEVtYWlsU3RyDQogICAgcGFzc3dvcmQ6IHN0cg0KDQoNCkByb3V0ZXIucG9zdCgiL3JlZ2lzdGVyIiwgcmVzcG9uc2VfbW9kZWw9c2NoZW1hcy5Vc2VyKQ0KZGVmIHJlZ2lzdGVyX3VzZXIoDQogICAgdXNlcjogVXNlclJlZ2lzdGVyLA0KICAgIGRiOiBTZXNzaW9uID0gRGVwZW5kcyhkZXBlbmRlbmNpZXMuZ2V0X2RiKSwNCik6DQogICAgaWYgY3J1ZC5nZXRfdXNlcl9ieV91c2VybmFtZShkYiwgdXNlcm5hbWU9dXNlci51c2VybmFtZSkgb3IgY3J1ZC5nZXRfdXNlcl9ieV9lbWFpbCgNCiAgICAgICAgZGIsIGVtYWlsPXVzZXIuZW1haWwNCiAgICApOg0KICAgICAgICByYWlzZSBIVFRQRXhjZXB0aW9uKA0KICAgICAgICAgICAgc3RhdHVzX2NvZGU9NDAwLCBkZXRhaWw9IlVzZXJuYW1lIG9yIGVtYWlsIGFscmVhZHkgcmVnaXN0ZXJlZCINCiAgICAgICAgKQ0KICAgIGRiX3VzZXIgPSBjcnVkLmNyZWF0ZV91c2VyKA0KICAgICAgICBkYiwNCiAgICAgICAgdXNlcj1zY2hlbWFzLlVzZXJDcmVhdGUoDQogICAgICAgICAgICB1c2VybmFtZT11c2VyLnVzZXJuYW1lLA0KICAgICAgICAgICAgZW1haWw9dXNlci5lbWFpbCwNCiAgICAgICAgICAgIHBhc3N3b3JkPXVzZXIucGFzc3dvcmQsDQogICAgICAgICAgICByb2xlPSJ1c2VyIiwNCiAgICAgICAgKSwNCiAgICApDQogICAgcmV0dXJuIGRiX3VzZXINCg=="
            )
        )

    # Writing file: user.py
    with open(os.path.join(target_folder, "api", "user.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "ZnJvbSBmYXN0YXBpIGltcG9ydCBBUElSb3V0ZXIsIERlcGVuZHMsIEhUVFBFeGNlcHRpb24NCmZyb20gcHlkYW50aWMgaW1wb3J0IEJhc2VNb2RlbA0KZnJvbSBzcWxhbGNoZW15Lm9ybSBpbXBvcnQgU2Vzc2lvbg0KZnJvbSB0eXBpbmcgaW1wb3J0IExpc3QNCmZyb20gYXBwIGltcG9ydCBjcnVkLCBzY2hlbWFzLCBtb2RlbHMNCmZyb20gYXBwLmNvcmUgaW1wb3J0IGRlcGVuZGVuY2llcywgdXRpbHMNCg0Kcm91dGVyID0gQVBJUm91dGVyKHByZWZpeD0iIiwgdGFncz1bInVzZXIiXSkNCg0KDQpAcm91dGVyLmdldCgiL3VzZXJzL21lLyIsIHJlc3BvbnNlX21vZGVsPXNjaGVtYXMuVXNlcikNCmRlZiByZWFkX3VzZXJzX21lKGN1cnJlbnRfdXNlcjogbW9kZWxzLlVzZXIgPSBEZXBlbmRzKGRlcGVuZGVuY2llcy5nZXRfY3VycmVudF91c2VyKSk6DQogICAgcmV0dXJuIGN1cnJlbnRfdXNlcg0KDQoNCkByb3V0ZXIucG9zdCgiL3VzZXJzLyIsIHJlc3BvbnNlX21vZGVsPXNjaGVtYXMuVXNlcikNCmRlZiBjcmVhdGVfdXNlcigNCiAgICB1c2VyOiBzY2hlbWFzLlVzZXJDcmVhdGUsDQogICAgZGI6IFNlc3Npb24gPSBEZXBlbmRzKGRlcGVuZGVuY2llcy5nZXRfZGIpLA0KICAgIGN1cnJlbnRfdXNlcjogbW9kZWxzLlVzZXIgPSBEZXBlbmRzKA0KICAgICAgICBkZXBlbmRlbmNpZXMuY2hlY2tfdXNlcl9yb2xlKFsic3VwZXJhZG1pbiIsICJhZG1pbiJdKSwNCiAgICApLA0KKToNCg0KICAgIGlmIGNydWQuZ2V0X3VzZXJfYnlfZW1haWwoZGIsIGVtYWlsPXVzZXIuZW1haWwpOg0KICAgICAgICByYWlzZSBIVFRQRXhjZXB0aW9uKHN0YXR1c19jb2RlPTQwMCwgZGV0YWlsPSJFbWFpbCBhbHJlYWR5IHJlZ2lzdGVyZWQiKQ0KICAgIGlmIGNydWQuZ2V0X3VzZXJfYnlfdXNlcm5hbWUoZGIsIHVzZXJuYW1lPXVzZXIudXNlcm5hbWUpOg0KICAgICAgICByYWlzZSBIVFRQRXhjZXB0aW9uKHN0YXR1c19jb2RlPTQwMCwgZGV0YWlsPSJVc2VybmFtZSBhbHJlYWR5IHJlZ2lzdGVyZWQiKQ0KICAgIHJldHVybiBjcnVkLmNyZWF0ZV91c2VyKGRiPWRiLCB1c2VyPXVzZXIpDQoNCg0KQHJvdXRlci5nZXQoIi91c2Vycy97dXNlcl9pZH0iLCByZXNwb25zZV9tb2RlbD1zY2hlbWFzLlVzZXIpDQpkZWYgcmVhZF91c2VyKA0KICAgIHVzZXJfaWQ6IGludCwNCiAgICBkYjogU2Vzc2lvbiA9IERlcGVuZHMoZGVwZW5kZW5jaWVzLmdldF9kYiksDQogICAgY3VycmVudF91c2VyOiBtb2RlbHMuVXNlciA9IERlcGVuZHMoDQogICAgICAgIGRlcGVuZGVuY2llcy5jaGVja191c2VyX3JvbGUoWyJzdXBlcmFkbWluIiwgImFkbWluIl0pDQogICAgKSwNCik6DQogICAgZGJfdXNlciA9IGNydWQuZ2V0X3VzZXIoZGIsIHVzZXJfaWQ9dXNlcl9pZCkNCiAgICBpZiBkYl91c2VyIGlzIE5vbmU6DQogICAgICAgIHJhaXNlIEhUVFBFeGNlcHRpb24oc3RhdHVzX2NvZGU9NDA0LCBkZXRhaWw9IlVzZXIgbm90IGZvdW5kIikNCiAgICByZXR1cm4gZGJfdXNlcg0KDQoNCkByb3V0ZXIucHV0KCIvdXNlcnMve3VzZXJfaWR9IiwgcmVzcG9uc2VfbW9kZWw9c2NoZW1hcy5Vc2VyKQ0KZGVmIHVwZGF0ZV91c2VyKA0KICAgIHVzZXJfaWQ6IGludCwNCiAgICB1c2VyOiBzY2hlbWFzLlVzZXJVcGRhdGUsDQogICAgZGI6IFNlc3Npb24gPSBEZXBlbmRzKGRlcGVuZGVuY2llcy5nZXRfZGIpLA0KICAgIGN1cnJlbnRfdXNlcjogbW9kZWxzLlVzZXIgPSBEZXBlbmRzKA0KICAgICAgICBkZXBlbmRlbmNpZXMuY2hlY2tfdXNlcl9yb2xlKFsic3VwZXJhZG1pbiIsICJhZG1pbiJdKQ0KICAgICksDQopOg0KICAgIGRiX3VzZXIgPSBjcnVkLnVwZGF0ZV91c2VyKGRiLCB1c2VyX2lkPXVzZXJfaWQsIHVzZXJfdXBkYXRlPXVzZXIpDQogICAgaWYgZGJfdXNlciBpcyBOb25lOg0KICAgICAgICByYWlzZSBIVFRQRXhjZXB0aW9uKHN0YXR1c19jb2RlPTQwNCwgZGV0YWlsPSJVc2VyIG5vdCBmb3VuZCIpDQogICAgcmV0dXJuIGRiX3VzZXINCg0KDQpAcm91dGVyLmRlbGV0ZSgiL3VzZXJzL3t1c2VyX2lkfSIsIHJlc3BvbnNlX21vZGVsPXNjaGVtYXMuVXNlcikNCmRlZiBkZWxldGVfdXNlcigNCiAgICB1c2VyX2lkOiBpbnQsDQogICAgZGI6IFNlc3Npb24gPSBEZXBlbmRzKGRlcGVuZGVuY2llcy5nZXRfZGIpLA0KICAgIGN1cnJlbnRfdXNlcjogbW9kZWxzLlVzZXIgPSBEZXBlbmRzKA0KICAgICAgICBkZXBlbmRlbmNpZXMuY2hlY2tfdXNlcl9yb2xlKFsic3VwZXJhZG1pbiIsICJhZG1pbiJdKQ0KICAgICksDQopOg0KICAgIGRiX3VzZXIgPSBjcnVkLmRlbGV0ZV91c2VyKGRiLCB1c2VyX2lkPXVzZXJfaWQpDQogICAgaWYgZGJfdXNlciBpcyBOb25lOg0KICAgICAgICByYWlzZSBIVFRQRXhjZXB0aW9uKHN0YXR1c19jb2RlPTQwNCwgZGV0YWlsPSJVc2VyIG5vdCBmb3VuZCIpDQogICAgcmV0dXJuIGRiX3VzZXINCg0KDQpAcm91dGVyLmdldCgiL3VzZXJzLyIsIHJlc3BvbnNlX21vZGVsPUxpc3Rbc2NoZW1hcy5Vc2VyXSkNCmRlZiByZWFkX3VzZXJzKA0KICAgIHBhZ2U6IGludCA9IDAsDQogICAgcGVyX3BhZ2U6IGludCA9IDEwLA0KICAgIGRiOiBTZXNzaW9uID0gRGVwZW5kcyhkZXBlbmRlbmNpZXMuZ2V0X2RiKSwNCiAgICBjdXJyZW50X3VzZXI6IG1vZGVscy5Vc2VyID0gRGVwZW5kcygNCiAgICAgICAgZGVwZW5kZW5jaWVzLmNoZWNrX3VzZXJfcm9sZShbInN1cGVyYWRtaW4iLCAiYWRtaW4iXSkNCiAgICApLA0KKToNCiAgICB1c2VycyA9IGNydWQuZ2V0X3VzZXJzKGRiLCBza2lwPXBhZ2UgKiBwZXJfcGFnZSwgbGltaXQ9cGVyX3BhZ2UpDQogICAgcmV0dXJuIHVzZXJzDQoNCg0KY2xhc3MgVXNlckNoYW5nZVBhc3N3b3JkKEJhc2VNb2RlbCk6DQogICAgb2xkX3Bhc3N3b3JkOiBzdHINCiAgICBuZXdfcGFzc3dvcmQ6IHN0cg0KICAgIGNvbmZpcm1fcGFzc3dvcmQ6IHN0cg0KDQoNCkByb3V0ZXIucHV0KCIvdXNlcnMvY2hhbmdlLXBhc3N3b3JkLyIsIHJlc3BvbnNlX21vZGVsPXNjaGVtYXMuVXNlcikNCmRlZiBjaGFuZ2VfcGFzc3dvcmQoDQogICAgZGF0YTogVXNlckNoYW5nZVBhc3N3b3JkLA0KICAgIGRiOiBTZXNzaW9uID0gRGVwZW5kcyhkZXBlbmRlbmNpZXMuZ2V0X2RiKSwNCiAgICBjdXJyZW50X3VzZXI6IG1vZGVscy5Vc2VyID0gRGVwZW5kcyhkZXBlbmRlbmNpZXMuZ2V0X2N1cnJlbnRfYWN0aXZlX3VzZXIpLA0KKToNCiAgICBpZiBub3QgdXRpbHMudmVyaWZ5X3Bhc3N3b3JkKGRhdGEub2xkX3Bhc3N3b3JkLCBzdHIoY3VycmVudF91c2VyLmhhc2hlZF9wYXNzd29yZCkpOg0KICAgICAgICByYWlzZSBIVFRQRXhjZXB0aW9uKHN0YXR1c19jb2RlPTQwMCwgZGV0YWlsPSJJbmNvcnJlY3QgcGFzc3dvcmQiKQ0KICAgIGlmIGRhdGEubmV3X3Bhc3N3b3JkICE9IGRhdGEuY29uZmlybV9wYXNzd29yZDoNCiAgICAgICAgcmFpc2UgSFRUUEV4Y2VwdGlvbihzdGF0dXNfY29kZT00MDAsIGRldGFpbD0iUGFzc3dvcmRzIGRvIG5vdCBtYXRjaCIpDQogICAgY2hhbmdlZF9kYl91c2VyID0gY3J1ZC51cGRhdGVfdXNlcigNCiAgICAgICAgZGI9ZGIsDQogICAgICAgIHVzZXJfaWQ9Y3VycmVudF91c2VyLmlkLCAgIyB0eXBlOiBpZ25vcmUNCiAgICAgICAgdXNlcl91cGRhdGU9c2NoZW1hcy5Vc2VyVXBkYXRlKA0KICAgICAgICAgICAgcGFzc3dvcmQ9ZGF0YS5uZXdfcGFzc3dvcmQsDQogICAgICAgICksDQogICAgKQ0KICAgIHJldHVybiBjaGFuZ2VkX2RiX3VzZXINCg=="
            )
        )

    # Writing file: __init__.py
    with open(os.path.join(target_folder, "api", "__init__.py"), "wb") as f:
        f.write(base64.b64decode(""))

    # Creating directory: core
    os.makedirs(os.path.join(target_folder, "core"), exist_ok=True)

    # Writing file: config.py
    with open(os.path.join(target_folder, "core", "config.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "ZnJvbSBweWRhbnRpYyBpbXBvcnQgQmFzZU1vZGVsDQppbXBvcnQgeWFtbA0KDQpjbGFzcyBNWVNRTFNldHRpbmdzKEJhc2VNb2RlbCk6DQogICAgSE9TVDogc3RyDQogICAgUE9SVDogaW50DQogICAgVVNFUjogc3RyDQogICAgUEFTU1dPUkQ6IHN0cg0KICAgIERBVEFCQVNFOiBzdHINCg0KY2xhc3MgSldUU2V0dGluZ3MoQmFzZU1vZGVsKToNCiAgICBTRUNSRVRfS0VZOiBzdHINCiAgICBBTEdPUklUSE06IHN0cg0KICAgIEVYUElSRV9NSU5VVEVTOiBpbnQNCg0KY2xhc3MgQXBwU2V0dGluZ3MoQmFzZU1vZGVsKToNCiAgICBOQU1FOiBzdHINCiAgICBWRVJTSU9OOiBzdHINCiAgICBERVNDUklQVElPTjogc3RyDQoNCmNsYXNzIEFwcENvbmZpZyhCYXNlTW9kZWwpOg0KICAgIEFQUDogQXBwU2V0dGluZ3MNCiAgICBNWVNRTDogTVlTUUxTZXR0aW5ncw0KICAgIEpXVDogSldUU2V0dGluZ3MNCg0KZGVmIF9sb2FkX2NvbmZpZ19mcm9tX2ZpbGUoZmlsZV9wYXRoKToNCiAgICB3aXRoIG9wZW4oZmlsZV9wYXRoLCAncicpIGFzIGZpbGU6DQogICAgICAgIGNvbmZpZyA9IHlhbWwuc2FmZV9sb2FkKGZpbGUpDQogICAgcmV0dXJuIEFwcENvbmZpZygqKmNvbmZpZykNCg0KQ09ORklHID0gX2xvYWRfY29uZmlnX2Zyb21fZmlsZSgnY29uZmlnLnlhbWwnKQ0KDQoNCg=="
            )
        )

    # Writing file: database.py
    with open(os.path.join(target_folder, "core", "database.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "ZnJvbSBzcWxhbGNoZW15IGltcG9ydCBjcmVhdGVfZW5naW5lCmZyb20gc3FsYWxjaGVteS5lbmdpbmUgaW1wb3J0IFVSTApmcm9tIHNxbGFsY2hlbXkuZXh0LmRlY2xhcmF0aXZlIGltcG9ydCBkZWNsYXJhdGl2ZV9iYXNlCmZyb20gc3FsYWxjaGVteS5vcm0gaW1wb3J0IHNlc3Npb25tYWtlcgpmcm9tIGFwcC5jb3JlLmNvbmZpZyBpbXBvcnQgQ09ORklHCgpTUUxBTENIRU1ZX0RBVEFCQVNFX1VSTCA9IFVSTC5jcmVhdGUoCiAgICAibXlzcWwiLAogICAgdXNlcm5hbWU9Q09ORklHLk1ZU1FMLlVTRVIsCiAgICBwYXNzd29yZD1DT05GSUcuTVlTUUwuUEFTU1dPUkQsCiAgICBob3N0PUNPTkZJRy5NWVNRTC5IT1NULAogICAgcG9ydD0gQ09ORklHLk1ZU1FMLlBPUlQsCiAgICBkYXRhYmFzZT1DT05GSUcuTVlTUUwuREFUQUJBU0UKKQoKZW5naW5lID0gY3JlYXRlX2VuZ2luZSgKICAgIFNRTEFMQ0hFTVlfREFUQUJBU0VfVVJMLAogICAgcG9vbF9zaXplPTEwLCAgIyDorr7nva7ov57mjqXmsaDlpKflsI/kuLoxMAogICAgbWF4X292ZXJmbG93PTIwLCAgIyDorr7nva7lhYHorrjnmoTmnIDlpKfov57mjqXmlbDvvIjotoXlh7rov57mjqXmsaDlpKflsI/ml7bvvIkKICAgIHBvb2xfdGltZW91dD0zMCwgICMg6K6+572u6I635Y+W6L+e5o6l55qE6LaF5pe25pe26Ze077yI56eS77yJCiAgICBwb29sX3JlY3ljbGU9MzYwMCwgICMg6K6+572u6L+e5o6l55qE5Zue5pS25pe26Ze077yI56eS77yJCiAgICBwb29sX3ByZV9waW5nPVRydWUsICAjIOWQr+eUqOi/nuaOpeS/nea0u+acuuWItu+8jOiHquWKqOajgOafpei/nuaOpeaYr+WQpuacieaViAogICAgZWNobz1GYWxzZSwgICMg5b2T5Li6VHJ1ZeaXtu+8jOWwhuaJk+WNsOaJgOacieS4juaVsOaNruW6k+S6pOS6kueahFNRTOivreWPpQopCgpTZXNzaW9uTG9jYWwgPSBzZXNzaW9ubWFrZXIoYXV0b2NvbW1pdD1GYWxzZSwgYXV0b2ZsdXNoPUZhbHNlLCBiaW5kPWVuZ2luZSkKCkJhc2UgPSBkZWNsYXJhdGl2ZV9iYXNlKCkK"
            )
        )

    # Writing file: dependencies.py
    with open(os.path.join(target_folder, "core", "dependencies.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "ZnJvbSB0eXBpbmcgaW1wb3J0IExpc3QNCmZyb20gZmFzdGFwaSBpbXBvcnQgRGVwZW5kcywgSFRUUEV4Y2VwdGlvbiwgc3RhdHVzDQpmcm9tIGZhc3RhcGkuc2VjdXJpdHkgaW1wb3J0IE9BdXRoMlBhc3N3b3JkQmVhcmVyDQpmcm9tIGFwcC5jb3JlLnNlY3VyaXR5IGltcG9ydCB2ZXJpZnlfYWNjZXNzX3Rva2VuDQpmcm9tIGFwcCBpbXBvcnQgY3J1ZCwgbW9kZWxzDQpmcm9tIGFwcC5jb3JlLmRhdGFiYXNlIGltcG9ydCBTZXNzaW9uTG9jYWwNCmZyb20gc3FsYWxjaGVteS5vcm0gaW1wb3J0IFNlc3Npb24NCg0KDQpkZWYgZ2V0X2RiKCk6DQogICAgZGIgPSBTZXNzaW9uTG9jYWwoKQ0KICAgIHRyeToNCiAgICAgICAgeWllbGQgZGINCiAgICBmaW5hbGx5Og0KICAgICAgICBkYi5jbG9zZSgpDQoNCg0Kb2F1dGgyX3NjaGVtZSA9IE9BdXRoMlBhc3N3b3JkQmVhcmVyKHRva2VuVXJsPSJsb2dpbi90b2tlbiIpDQoNCg0KZGVmIGdldF9jdXJyZW50X3VzZXIoDQogICAgdG9rZW46IHN0ciA9IERlcGVuZHMob2F1dGgyX3NjaGVtZSksDQogICAgZGI6IFNlc3Npb24gPSBEZXBlbmRzKGdldF9kYiksDQopOg0KICAgIGNyZWRlbnRpYWxzX2V4Y2VwdGlvbiA9IEhUVFBFeGNlcHRpb24oDQogICAgICAgIHN0YXR1c19jb2RlPXN0YXR1cy5IVFRQXzQwMV9VTkFVVEhPUklaRUQsDQogICAgICAgIGRldGFpbD0iQ291bGQgbm90IHZhbGlkYXRlIGNyZWRlbnRpYWxzIiwNCiAgICAgICAgaGVhZGVycz17IldXVy1BdXRoZW50aWNhdGUiOiAiQmVhcmVyIn0sDQogICAgKQ0KICAgIHRva2VuX2RhdGEgPSB2ZXJpZnlfYWNjZXNzX3Rva2VuKHRva2VuLCBjcmVkZW50aWFsc19leGNlcHRpb24pDQogICAgdXNlciA9IGNydWQuZ2V0X3VzZXJfYnlfdXNlcm5hbWUoZGIsIHVzZXJuYW1lPXRva2VuX2RhdGEudXNlcm5hbWUpDQogICAgaWYgdXNlciBpcyBOb25lOg0KICAgICAgICByYWlzZSBjcmVkZW50aWFsc19leGNlcHRpb24NCiAgICByZXR1cm4gdXNlcg0KDQoNCmRlZiBnZXRfY3VycmVudF9hY3RpdmVfdXNlcigNCiAgICB0b2tlbjogc3RyID0gRGVwZW5kcyhvYXV0aDJfc2NoZW1lKSwNCiAgICBkYjogU2Vzc2lvbiA9IERlcGVuZHMoZ2V0X2RiKSwNCik6DQogICAgY3JlZGVudGlhbHNfZXhjZXB0aW9uID0gSFRUUEV4Y2VwdGlvbigNCiAgICAgICAgc3RhdHVzX2NvZGU9c3RhdHVzLkhUVFBfNDAxX1VOQVVUSE9SSVpFRCwNCiAgICAgICAgZGV0YWlsPSJDb3VsZCBub3QgdmFsaWRhdGUgY3JlZGVudGlhbHMiLA0KICAgICAgICBoZWFkZXJzPXsiV1dXLUF1dGhlbnRpY2F0ZSI6ICJCZWFyZXIifSwNCiAgICApDQogICAgdG9rZW5fZGF0YSA9IHZlcmlmeV9hY2Nlc3NfdG9rZW4odG9rZW4sIGNyZWRlbnRpYWxzX2V4Y2VwdGlvbikNCiAgICB1c2VyID0gY3J1ZC5nZXRfdXNlcl9ieV91c2VybmFtZShkYiwgdXNlcm5hbWU9dG9rZW5fZGF0YS51c2VybmFtZSkNCiAgICBpZiB1c2VyIGlzIE5vbmU6DQogICAgICAgIHJhaXNlIGNyZWRlbnRpYWxzX2V4Y2VwdGlvbg0KICAgIGlmIGJvb2wodXNlci5kaXNhYmxlZCk6DQogICAgICAgIHJhaXNlIEhUVFBFeGNlcHRpb24oDQogICAgICAgICAgICBzdGF0dXNfY29kZT1zdGF0dXMuSFRUUF80MDFfVU5BVVRIT1JJWkVELA0KICAgICAgICAgICAgZGV0YWlsPSJZb3UgaGF2ZSBiZWVuIGRpc2FibGVkLiBQbGVhc2UgY29udGFjdCB0aGUgYWRtaW5pc3RyYXRvci4iLA0KICAgICAgICApDQogICAgcmV0dXJuIHVzZXINCg0KDQpkZWYgY2hlY2tfdXNlcl9yb2xlKHJlcXVpcmVkX3JvbGVzOiBMaXN0W3N0cl0pOg0KICAgIGRlZiByb2xlX2NoZWNrZXIoY3VycmVudF91c2VyOiBtb2RlbHMuVXNlciA9IERlcGVuZHMoZ2V0X2N1cnJlbnRfYWN0aXZlX3VzZXIpKToNCiAgICAgICAgaWYgY3VycmVudF91c2VyLnJvbGUgbm90IGluIHJlcXVpcmVkX3JvbGVzOg0KICAgICAgICAgICAgcmFpc2UgSFRUUEV4Y2VwdGlvbigNCiAgICAgICAgICAgICAgICBzdGF0dXNfY29kZT1zdGF0dXMuSFRUUF80MDNfRk9SQklEREVOLCBkZXRhaWw9Ik5vdCBlbm91Z2ggcGVybWlzc2lvbnMiDQogICAgICAgICAgICApDQogICAgICAgIHJldHVybiBjdXJyZW50X3VzZXINCg0KICAgIHJldHVybiByb2xlX2NoZWNrZXINCg=="
            )
        )

    # Writing file: log.py
    with open(os.path.join(target_folder, "core", "log.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "aW1wb3J0IGxvZ2dpbmcNCg0KbG9nZ2luZy5iYXNpY0NvbmZpZygNCiAgICBsZXZlbD1sb2dnaW5nLklORk8sDQogICAgZm9ybWF0PSIlKGxldmVsbmFtZSlzOiAgICUoYXNjdGltZSlzICAgJShtZXNzYWdlKXMiLA0KICAgIGhhbmRsZXJzPVsNCiAgICAgICAgbG9nZ2luZy5TdHJlYW1IYW5kbGVyKCksDQogICAgICAgIGxvZ2dpbmcuRmlsZUhhbmRsZXIoImxvZy50eHQiLCBlbmNvZGluZz0idXRmLTgiKSwNCiAgICBdLA0KKQ0KDQojIOS9v+eUqGxvZ2dlcuWunuS+iw0KbG9nZ2VyID0gbG9nZ2luZy5nZXRMb2dnZXIoKQ=="
            )
        )

    # Writing file: security.py
    with open(os.path.join(target_folder, "core", "security.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "aW1wb3J0IGp3dA0KZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZXRpbWUsIHRpbWVkZWx0YQ0KZnJvbSB0eXBpbmcgaW1wb3J0IE9wdGlvbmFsDQpmcm9tIHB5ZGFudGljIGltcG9ydCBCYXNlTW9kZWwNCmZyb20gYXBwLmNvcmUuY29uZmlnIGltcG9ydCBDT05GSUcNCg0KDQpjbGFzcyBUb2tlbkRhdGEoQmFzZU1vZGVsKToNCiAgICB1c2VybmFtZTogc3RyDQoNCg0KY2xhc3MgVG9rZW4oQmFzZU1vZGVsKToNCiAgICBhY2Nlc3NfdG9rZW46IHN0cg0KICAgIHRva2VuX3R5cGU6IHN0cg0KDQoNCmRlZiBjcmVhdGVfYWNjZXNzX3Rva2VuKGRhdGE6IGRpY3QsIGV4cGlyZXNfZGVsdGE6IHRpbWVkZWx0YSB8IE5vbmUgPSBOb25lKToNCiAgICB0b19lbmNvZGUgPSBkYXRhLmNvcHkoKQ0KICAgIGlmIGV4cGlyZXNfZGVsdGE6DQogICAgICAgIGV4cGlyZSA9IGRhdGV0aW1lLm5vdygpICsgZXhwaXJlc19kZWx0YQ0KICAgIGVsc2U6DQogICAgICAgIGV4cGlyZSA9IGRhdGV0aW1lLm5vdygpICsgdGltZWRlbHRhKG1pbnV0ZXM9Q09ORklHLkpXVC5FWFBJUkVfTUlOVVRFUykNCiAgICB0b19lbmNvZGUudXBkYXRlKHsiZXhwIjogZXhwaXJlfSkNCiAgICBlbmNvZGVkX2p3dCA9IGp3dC5lbmNvZGUoDQogICAgICAgIHRvX2VuY29kZSwgQ09ORklHLkpXVC5TRUNSRVRfS0VZLCBhbGdvcml0aG09Q09ORklHLkpXVC5BTEdPUklUSE0NCiAgICApDQogICAgcmV0dXJuIGVuY29kZWRfand0DQoNCg0KZGVmIHZlcmlmeV9hY2Nlc3NfdG9rZW4odG9rZW46IHN0ciwgY3JlZGVudGlhbHNfZXhjZXB0aW9uKToNCiAgICB0cnk6DQogICAgICAgIHBheWxvYWQgPSBqd3QuZGVjb2RlKA0KICAgICAgICAgICAgdG9rZW4sIENPTkZJRy5KV1QuU0VDUkVUX0tFWSwgYWxnb3JpdGhtcz1bQ09ORklHLkpXVC5BTEdPUklUSE1dDQogICAgICAgICkNCiAgICAgICAgdXNlcm5hbWU6IHN0ciA9IHBheWxvYWQuZ2V0KCJzdWIiKQ0KICAgICAgICBpZiB1c2VybmFtZSBpcyBOb25lOg0KICAgICAgICAgICAgcmFpc2UgY3JlZGVudGlhbHNfZXhjZXB0aW9uDQogICAgICAgIHRva2VuX2RhdGEgPSBUb2tlbkRhdGEodXNlcm5hbWU9dXNlcm5hbWUpDQogICAgZXhjZXB0IGp3dC5QeUpXVEVycm9yOg0KICAgICAgICByYWlzZSBjcmVkZW50aWFsc19leGNlcHRpb24NCiAgICByZXR1cm4gdG9rZW5fZGF0YQ0K"
            )
        )

    # Writing file: utils.py
    with open(os.path.join(target_folder, "core", "utils.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "aW1wb3J0IGJjcnlwdA0KDQpkZWYgaGFzaF9wYXNzd29yZChwYXNzd29yZDogc3RyKSAtPiBzdHI6DQogICAgIiIiSGFzaCBhIHBhc3N3b3JkIGZvciBzdG9yaW5nLiIiIg0KICAgIHNhbHQgPSBiY3J5cHQuZ2Vuc2FsdCgpDQogICAgaGFzaGVkID0gYmNyeXB0Lmhhc2hwdyhwYXNzd29yZC5lbmNvZGUoJ3V0Zi04JyksIHNhbHQpDQogICAgcmV0dXJuIGhhc2hlZC5kZWNvZGUoJ3V0Zi04JykNCg0KZGVmIHZlcmlmeV9wYXNzd29yZChwbGFpbl9wYXNzd29yZDogc3RyLCBoYXNoZWRfcGFzc3dvcmQ6IHN0cikgLT4gYm9vbDoNCiAgICAiIiJWZXJpZnkgYSBzdG9yZWQgcGFzc3dvcmQgYWdhaW5zdCBvbmUgcHJvdmlkZWQgYnkgdXNlci4iIiINCiAgICByZXR1cm4gYmNyeXB0LmNoZWNrcHcocGxhaW5fcGFzc3dvcmQuZW5jb2RlKCd1dGYtOCcpLCBoYXNoZWRfcGFzc3dvcmQuZW5jb2RlKCd1dGYtOCcpKQ0K"
            )
        )

    # Writing file: __init__.py
    with open(os.path.join(target_folder, "core", "__init__.py"), "wb") as f:
        f.write(base64.b64decode(""))

    # Creating directory: crud
    os.makedirs(os.path.join(target_folder, "crud"), exist_ok=True)

    # Writing file: user.py
    with open(os.path.join(target_folder, "crud", "user.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "ZnJvbSB0eXBpbmcgaW1wb3J0IExpc3QKZnJvbSBzcWxhbGNoZW15Lm9ybSBpbXBvcnQgU2Vzc2lvbgpmcm9tIGFwcCBpbXBvcnQgc2NoZW1hcywgbW9kZWxzCmZyb20gYXBwLmNvcmUgaW1wb3J0IHV0aWxzCgoKZGVmIGdldF91c2VyKGRiOiBTZXNzaW9uLCB1c2VyX2lkOiBpbnQpIC0+IG1vZGVscy5Vc2VyIHwgTm9uZToKICAgIHJldHVybiBkYi5xdWVyeShtb2RlbHMuVXNlcikuZmlsdGVyKG1vZGVscy5Vc2VyLmlkID09IHVzZXJfaWQpLmZpcnN0KCkKCgpkZWYgZ2V0X3VzZXJfYnlfdXNlcm5hbWUoZGI6IFNlc3Npb24sIHVzZXJuYW1lOiBzdHIpIC0+IG1vZGVscy5Vc2VyIHwgTm9uZToKICAgIHJldHVybiBkYi5xdWVyeShtb2RlbHMuVXNlcikuZmlsdGVyKG1vZGVscy5Vc2VyLnVzZXJuYW1lID09IHVzZXJuYW1lKS5maXJzdCgpCgoKZGVmIGdldF91c2VyX2J5X2VtYWlsKGRiOiBTZXNzaW9uLCBlbWFpbDogc3RyKSAtPiBtb2RlbHMuVXNlciB8IE5vbmU6CiAgICByZXR1cm4gZGIucXVlcnkobW9kZWxzLlVzZXIpLmZpbHRlcihtb2RlbHMuVXNlci5lbWFpbCA9PSBlbWFpbCkuZmlyc3QoKQoKCmRlZiBnZXRfdXNlcnMoZGI6IFNlc3Npb24sIHNraXA6IGludCA9IDAsIGxpbWl0OiBpbnQgPSAxMCkgLT4gTGlzdFttb2RlbHMuVXNlcl0gfCBOb25lOgogICAgcmV0dXJuIGRiLnF1ZXJ5KG1vZGVscy5Vc2VyKS5vZmZzZXQoc2tpcCkubGltaXQobGltaXQpLmFsbCgpCgoKZGVmIGNyZWF0ZV91c2VyKGRiOiBTZXNzaW9uLCB1c2VyOiBzY2hlbWFzLlVzZXJDcmVhdGUpOgogICAgaGFzaGVkX3Bhc3N3b3JkID0gdXRpbHMuaGFzaF9wYXNzd29yZCh1c2VyLnBhc3N3b3JkKQogICAgZGJfdXNlciA9IG1vZGVscy5Vc2VyKAogICAgICAgIHVzZXJuYW1lPXVzZXIudXNlcm5hbWUsCiAgICAgICAgZW1haWw9dXNlci5lbWFpbCwKICAgICAgICBoYXNoZWRfcGFzc3dvcmQ9aGFzaGVkX3Bhc3N3b3JkLAogICAgICAgIGZ1bGxfbmFtZT11c2VyLmZ1bGxfbmFtZSwKICAgICAgICBkaXNhYmxlZD11c2VyLmRpc2FibGVkLAogICAgICAgIHJvbGU9dXNlci5yb2xlLAogICAgKQogICAgZGIuYWRkKGRiX3VzZXIpCiAgICBkYi5jb21taXQoKQogICAgZGIucmVmcmVzaChkYl91c2VyKQogICAgcmV0dXJuIGRiX3VzZXIKCgpkZWYgdXBkYXRlX3VzZXIoZGI6IFNlc3Npb24sIHVzZXJfaWQ6IGludCwgdXNlcl91cGRhdGU6IHNjaGVtYXMuVXNlclVwZGF0ZSk6CiAgICBkYl91c2VyID0gZGIucXVlcnkobW9kZWxzLlVzZXIpLmZpbHRlcihtb2RlbHMuVXNlci5pZCA9PSB1c2VyX2lkKS5maXJzdCgpCiAgICBpZiBkYl91c2VyIGlzIE5vbmU6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIHVwZGF0ZV9kYXRhID0gdXNlcl91cGRhdGUubW9kZWxfZHVtcChleGNsdWRlX3Vuc2V0PVRydWUpCiAgICBpZiAicGFzc3dvcmQiIGluIHVwZGF0ZV9kYXRhOgogICAgICAgIHVwZGF0ZV9kYXRhWyJoYXNoZWRfcGFzc3dvcmQiXSA9IHV0aWxzLmhhc2hfcGFzc3dvcmQodXBkYXRlX2RhdGFbInBhc3N3b3JkIl0pCiAgICAgICAgZGVsIHVwZGF0ZV9kYXRhWyJwYXNzd29yZCJdCiAgICBmb3Iga2V5LCB2YWx1ZSBpbiB1cGRhdGVfZGF0YS5pdGVtcygpOgogICAgICAgIHNldGF0dHIoZGJfdXNlciwga2V5LCB2YWx1ZSkKICAgIGRiLmNvbW1pdCgpCiAgICBkYi5yZWZyZXNoKGRiX3VzZXIpCiAgICByZXR1cm4gZGJfdXNlcgoKCmRlZiBkZWxldGVfdXNlcihkYjogU2Vzc2lvbiwgdXNlcl9pZDogaW50KToKICAgIGRiX3VzZXIgPSBkYi5xdWVyeShtb2RlbHMuVXNlcikuZmlsdGVyKG1vZGVscy5Vc2VyLmlkID09IHVzZXJfaWQpLmZpcnN0KCkKICAgIGlmIGRiX3VzZXIgaXMgTm9uZToKICAgICAgICByZXR1cm4gTm9uZQogICAgZGIuZGVsZXRlKGRiX3VzZXIpCiAgICBkYi5jb21taXQoKQogICAgcmV0dXJuIGRiX3VzZXIKCgpkZWYgYXV0aGVudGljYXRlX3VzZXIoZGI6IFNlc3Npb24sIHVzZXJuYW1lOiBzdHIsIHBhc3N3b3JkOiBzdHIpIC0+IG1vZGVscy5Vc2VyIHwgTm9uZToKICAgIHVzZXIgPSBnZXRfdXNlcl9ieV91c2VybmFtZShkYiwgdXNlcm5hbWUpCiAgICBpZiB1c2VyIGFuZCB1dGlscy52ZXJpZnlfcGFzc3dvcmQocGFzc3dvcmQsIHN0cih1c2VyLmhhc2hlZF9wYXNzd29yZCkpOgogICAgICAgIHJldHVybiB1c2VyCiAgICByZXR1cm4gTm9uZQo="
            )
        )

    # Writing file: __init__.py
    with open(os.path.join(target_folder, "crud", "__init__.py"), "wb") as f:
        f.write(base64.b64decode("ZnJvbSAudXNlciBpbXBvcnQgKg=="))

    # Creating directory: models
    os.makedirs(os.path.join(target_folder, "models"), exist_ok=True)

    # Writing file: user.py
    with open(os.path.join(target_folder, "models", "user.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "aW1wb3J0IGVudW0NCmZyb20gc3FsYWxjaGVteSBpbXBvcnQgQ29sdW1uLCBJbnRlZ2VyLCBTdHJpbmcsIEJvb2xlYW4sIFRJTUVTVEFNUCwgZnVuYywgRW51bQ0KZnJvbSBhcHAuY29yZS5kYXRhYmFzZSBpbXBvcnQgQmFzZQ0KDQoNCmNsYXNzIFVzZXIoQmFzZSk6DQogICAgX190YWJsZW5hbWVfXyA9ICJ1c2VycyINCg0KICAgIGlkID0gQ29sdW1uKEludGVnZXIsIHByaW1hcnlfa2V5PVRydWUsIGluZGV4PVRydWUsIGF1dG9pbmNyZW1lbnQ9VHJ1ZSkNCiAgICB1c2VybmFtZSA9IENvbHVtbihTdHJpbmcoNTApLCB1bmlxdWU9VHJ1ZSwgbnVsbGFibGU9RmFsc2UpDQogICAgZW1haWwgPSBDb2x1bW4oU3RyaW5nKDEwMCksIHVuaXF1ZT1UcnVlLCBudWxsYWJsZT1GYWxzZSkNCiAgICBoYXNoZWRfcGFzc3dvcmQgPSBDb2x1bW4oU3RyaW5nKDI1NSksIG51bGxhYmxlPUZhbHNlKQ0KICAgIGZ1bGxfbmFtZSA9IENvbHVtbihTdHJpbmcoMTAwKSkNCiAgICBkaXNhYmxlZCA9IENvbHVtbihCb29sZWFuLCBkZWZhdWx0PUZhbHNlLCBudWxsYWJsZT1GYWxzZSkNCiAgICByb2xlID0gQ29sdW1uKFN0cmluZyg1MCksIG51bGxhYmxlPUZhbHNlLCBkZWZhdWx0PSJ1c2VyIikNCiAgICBjcmVhdGVkX2F0ID0gQ29sdW1uKFRJTUVTVEFNUCwgc2VydmVyX2RlZmF1bHQ9ZnVuYy5ub3coKSkNCiAgICB1cGRhdGVkX2F0ID0gQ29sdW1uKFRJTUVTVEFNUCwgc2VydmVyX2RlZmF1bHQ9ZnVuYy5ub3coKSwgb251cGRhdGU9ZnVuYy5ub3coKSkNCg=="
            )
        )

    # Writing file: __init__.py
    with open(os.path.join(target_folder, "models", "__init__.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "ZnJvbSBhcHAuY29yZS5kYXRhYmFzZSBpbXBvcnQgQmFzZSwgZW5naW5lDQpmcm9tIC51c2VyIGltcG9ydCAqDQoNCkJhc2UubWV0YWRhdGEuY3JlYXRlX2FsbChiaW5kPWVuZ2luZSkNCg=="
            )
        )

    # Creating directory: schemas
    os.makedirs(os.path.join(target_folder, "schemas"), exist_ok=True)

    # Writing file: user.py
    with open(os.path.join(target_folder, "schemas", "user.py"), "wb") as f:
        f.write(
            base64.b64decode(
                "ZnJvbSBweWRhbnRpYyBpbXBvcnQgQmFzZU1vZGVsLCBFbWFpbFN0cg0KZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZXRpbWUNCg0KDQpjbGFzcyBVc2VyQmFzZShCYXNlTW9kZWwpOg0KICAgIHVzZXJuYW1lOiBzdHINCiAgICBlbWFpbDogRW1haWxTdHINCiAgICBmdWxsX25hbWU6IHN0ciB8IE5vbmUgPSBOb25lDQogICAgZGlzYWJsZWQ6IGJvb2wgfCBOb25lID0gTm9uZQ0KICAgIHJvbGU6IHN0ciB8IE5vbmUgPSBOb25lDQoNCg0KY2xhc3MgVXNlckNyZWF0ZShVc2VyQmFzZSk6DQogICAgcGFzc3dvcmQ6IHN0cg0KDQoNCmNsYXNzIFVzZXJVcGRhdGUoVXNlckJhc2UpOg0KICAgIHVzZXJuYW1lOiBzdHIgfCBOb25lID0gTm9uZQ0KICAgIGVtYWlsOiBFbWFpbFN0ciB8IE5vbmUgPSBOb25lDQogICAgcGFzc3dvcmQ6IHN0ciB8IE5vbmUgPSBOb25lDQoNCg0KY2xhc3MgVXNlckluREJCYXNlKFVzZXJCYXNlKToNCiAgICBpZDogaW50DQogICAgY3JlYXRlZF9hdDogZGF0ZXRpbWUNCiAgICB1cGRhdGVkX2F0OiBkYXRldGltZQ0KDQogICAgY2xhc3MgQ29uZmlnOg0KICAgICAgICBmcm9tX2F0dHJpYnV0ZXMgPSBUcnVlDQoNCg0KY2xhc3MgVXNlcihVc2VySW5EQkJhc2UpOg0KICAgIHBhc3MNCg0KDQpjbGFzcyBVc2VySW5EQihVc2VySW5EQkJhc2UpOg0KICAgIGhhc2hlZF9wYXNzd29yZDogc3RyDQo="
            )
        )

    # Writing file: __init__.py
    with open(os.path.join(target_folder, "schemas", "__init__.py"), "wb") as f:
        f.write(base64.b64decode("ZnJvbSAudXNlciBpbXBvcnQgKg0K"))


def save_folder_to_file(folder_path, output_file):
    """
    将文件夹中的所有文件和文件结构保存到单个文件中。
    :param folder_path: 要保存的文件夹路径
    :param output_file: 保存输出的文件路径
    """
    folder_data = {}

    for root, dirs, files in os.walk(folder_path):
        relative_path = os.path.relpath(root, folder_path)
        folder_data[relative_path] = {"dirs": dirs, "files": {}}
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                encoded_content = base64.b64encode(f.read()).decode("utf-8")
                folder_data[relative_path]["files"][file] = encoded_content

    with open(output_file, "w") as f:
        json.dump(folder_data, f, indent=4)


def load_folder_from_file(input_file, target_folder):
    """
    从单个文件中恢复文件和文件结构。
    :param input_file: 输入的单个文件路径
    :param target_folder: 恢复文件的目标文件夹路径
    """
    with open(input_file, "r") as f:
        folder_data = json.load(f)

    for relative_path, contents in folder_data.items():
        current_path = os.path.join(target_folder, relative_path)
        os.makedirs(current_path, exist_ok=True)
        for dir in contents["dirs"]:
            os.makedirs(os.path.join(current_path, dir), exist_ok=True)
        for file, encoded_content in contents["files"].items():
            file_path = os.path.join(current_path, file)
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(encoded_content))


def init_app():
    try:
        print("\033[1;36mWelcome to App Configuration Wizard!\033[0m\n")

        # Collect user inputs
        app_name = (
            input(
                "\033[1mStep 1 of 8:\033[0m Enter the name of the application (default 'my_app'): "
            )
            or "my_app"
        )
        app_version = (
            input(
                "\033[1mStep 2 of 8:\033[0m Enter the version of the application (default '1.0.0'): "
            )
            or "1.0.0"
        )
        app_description = (
            input(
                "\033[1mStep 3 of 8:\033[0m Enter the description of the application (default 'A sample description.'): "
            )
            or "A sample description."
        )
        mysql_host = (
            input(
                "\033[1mStep 4 of 8:\033[0m Enter the host of the MySQL database (default 'localhost'): "
            )
            or "localhost"
        )
        mysql_port = (
            input(
                "\033[1mStep 5 of 8:\033[0m Enter the port of the MySQL database (default '3306'): "
            )
            or "3306"
        )
        mysql_user = (
            input(
                "\033[1mStep 6 of 8:\033[0m Enter the username of the MySQL database (default 'root'): "
            )
            or "root"
        )
        mysql_password = (
            input(
                "\033[1mStep 7 of 8:\033[0m Enter the password of the MySQL database (default 'fakepassword'): "
            )
            or "fakepassword"
        )
        app_database = (
            input(
                "\033[1mStep 8 of 8:\033[0m Enter the name of the application database (default 'my_db'): "
            )
            or "my_db"
        )
        jwt_secret_key = "".join(
            secrets.choice(string.ascii_letters + string.digits + "-_")
            for _ in range(24)
        )
        jwt_algorithm = "HS256"
        jwt_expiration = 360

        print("\n\033[92mConfiguration completed successfully!\033[0m\n")

        # Format data into dictionary
        config_data = {
            "APP": {
                "NAME": app_name,
                "VERSION": app_version,
                "DESCRIPTION": app_description,
            },
            "MYSQL": {
                "HOST": mysql_host,
                "PORT": int(mysql_port),
                "USER": mysql_user,
                "PASSWORD": mysql_password,
                "DATABASE": app_database,
            },
            "JWT": {
                "SECRET_KEY": jwt_secret_key,
                "ALGORITHM": jwt_algorithm,
                "EXPIRE_MINUTES": int(jwt_expiration),
            },
        }

        # Write data to YAML file
        with open("config.yaml", "w") as file:
            yaml.dump(config_data, file, sort_keys=False)

        print(
            "\033[94mGenerated config.yaml successfully, you can change it according to your needs.\033[0m\n"
        )

        # Placeholder for load_folder("app")
        load_folder("app")
        print("\033[94mGenerated app folder successfully.\033[0m\n")

        print("\033[1;35mHave a nice day!\033[0m")

    except ValueError as e:
        print(f"\033[91mError: {e}\033[0m")
        print(
            "\033[91mPlease ensure numeric inputs (like port number and JWT expiration) are valid.\033[0m"
        )
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
        print("\033[91mAn unexpected error occurred. Please try again.\033[0m")


def run_dev(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)


def run_prod(host: str = "0.0.0.0", port: int = 8000):
    uvicorn.run("app.main:app", host=host, port=port)


def create_model_module(module_name):
    module_filename = f"{module_name}.py"
    init_filename = "__init__.py"
    module_import_line = f"\nfrom .{module_name} import *"

    module_folder = os.path.join(os.path.dirname(__file__), "app", "models")
    module_file_path = os.path.join(module_folder, module_filename)
    init_file_path = os.path.join(module_folder, init_filename)

    # Create the model file with specific content
    with open(module_file_path, "w") as module_file:
        content = f"""# app/models/{module_name}.py
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from app.core.database import Base

# Create your model here
        """
        module_file.write(content)

    # Update the init file to import the new model
    with open(init_file_path, "a") as init_file:
        init_file.write(module_import_line)

    print(f"Created {module_filename} in models folder.")
    print(f"Updated {init_filename} in models folder.")


def create_api_module(module_name):
    module_filename = f"{module_name}.py"

    module_folder = os.path.join(os.path.dirname(__file__), "app", "api")
    module_file_path = os.path.join(module_folder, module_filename)

    # Create the api file with specific content
    with open(module_file_path, "w") as module_file:
        content = f"""# app/api/{module_name}.py
from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud,schemas,models
from app.core import dependencies

router = APIRouter(prefix="", tags=["{module_name}"])

# Create your api here
"""
        module_file.write(content)

    print(f"Created {module_filename} in api folder.")


def create_crud_module(module_name):
    module_filename = f"{module_name}.py"
    init_filename = "__init__.py"
    module_import_line = f"\nfrom .{module_name} import *"

    module_folder = os.path.join(os.path.dirname(__file__), "app", "crud")
    module_file_path = os.path.join(module_folder, module_filename)
    init_file_path = os.path.join(module_folder, init_filename)

    # Create the crud file with specific content
    with open(module_file_path, "w") as module_file:
        content = f"""# app/crud/{module_name}.py
from typing import List
from sqlalchemy.orm import Session
from app import schemas,models
from app.core import utils

# Create your crud here
        """
        module_file.write(content)

    # Update the init file to import the new crud module
    with open(init_file_path, "a") as init_file:
        # Check if the file ends with a newline
        init_file.write(module_import_line)

    print(f"Created {module_filename} in crud folder.")
    print(f"Updated {init_filename} in crud folder.")


def create_schema_module(module_name):
    module_filename = f"{module_name}.py"
    init_filename = "__init__.py"
    module_import_line = f"\nfrom .{module_name} import *"

    module_folder = os.path.join(os.path.dirname(__file__), "app", "schemas")
    module_file_path = os.path.join(module_folder, module_filename)
    init_file_path = os.path.join(module_folder, init_filename)

    # Create the schema file with specific content
    with open(module_file_path, "w") as module_file:
        content = f"""# app/schemas/{module_name}.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Create your schema here
        """
        module_file.write(content)

    with open(init_file_path, "a") as init_file:
        init_file.write(module_import_line)

    print(f"Created {module_filename} in schemas folder.")
    print(f"Updated {init_filename} in schemas folder.")


def create(name: str):
    create_model_module(name)
    create_api_module(name)
    create_crud_module(name)
    create_schema_module(name)


# 命令列表
commands = [
    {
        "name": "init",
        "func": init_app,
        "help": "Initialize the application.",
        "params": [],
    },
    {
        "name": "dev",
        "func": run_dev,
        "help": "Run the development server.",
        "params": [
            {
                "name": "host",
                "type": str,
                "help": "Host address to run the server on.",
                "default": "0.0.0.0",
            },
            {
                "name": "port",
                "type": int,
                "help": "Port number to run the server on.",
                "default": 8000,
            },
            {
                "name": "reload",
                "type": bool,
                "help": "Reload the server on code changes.",
                "default": True,
            },
        ],
    },
    {
        "name": "prod",
        "func": run_prod,
        "help": "Run the production server.",
        "params": [
            {
                "name": "host",
                "type": str,
                "help": "Host address to run the server on.",
                "default": "0.0.0.0",
            },
            {
                "name": "port",
                "type": int,
                "help": "Port number to run the server on.",
                "default": 5050,
            },
        ],
    },
    {
        "name": "create",
        "func": create,
        "help": "Create a new model, api, crud, and schema.",
        "params": [
            {
                "name": "name",
                "type": str,
                "help": "Name of the model, api, crud, and schema to create.",
                "default": None,
            }
        ],
    },
    {
        "name": "backup",
        "func": save_folder_to_py,
        "help": "backup the  folder to a py file.",
        "params": [
            {
                "name": "folder_path",
                "type": str,
                "help": "Path to the folder to backup.",
                "default": "app",
            }
        ],
    },
]


def main():
    parser = argparse.ArgumentParser(description="Manage.py utility script.")
    subparsers = parser.add_subparsers(dest="command")

    # 动态创建子命令
    for command in commands:
        subparser = subparsers.add_parser(command["name"], help=command["help"])
        for param in command["params"]:
            subparser.add_argument(
                f'--{param["name"]}',
                type=param.get("type"),
                help=param.get("help"),
                default=param.get("default"),
            )
        subparser.set_defaults(func=command["func"])

    args = parser.parse_args()

    if hasattr(args, "func"):
        command_func = args.func
        command_params = {
            k: v for k, v in vars(args).items() if k != "func" and k != "command"
        }
        command_func(**command_params)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
