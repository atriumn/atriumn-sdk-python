from ..client import run_task


async def extract_traits_document(input: dict, app: str, base_url: str, api_key: str):
    return await run_task("extract_traits_document", app=app, input=input, base_url=base_url, api_key=api_key)