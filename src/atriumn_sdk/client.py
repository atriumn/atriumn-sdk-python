import httpx


async def run_task(task: str, app: str, input: dict, base_url: str, api_key: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/v1/prompt",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"task": task, "app": app, "input": input},
        )
        response.raise_for_status()
        return response.json()