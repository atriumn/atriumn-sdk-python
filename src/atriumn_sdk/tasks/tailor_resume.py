from ..client import run_task


async def tailor_resume(input: dict, app: str, base_url: str, api_key: str):
    return await run_task("tailor_resume", app=app, input=input, base_url=base_url, api_key=api_key)