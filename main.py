import argparse
import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

from agent import DeepSeekMCPAgent


def get_api_key() -> str:
    # First, check environment variable
    import os

    env_key = os.getenv("DEEPSEEK_API_KEY")
    if env_key:
        return env_key.strip()

    # Second, check api_key.txt file
    key_path = Path(__file__).parent / "api_key.txt"
    if key_path.exists():
        return key_path.read_text(encoding="utf-8").strip()

    # Finally, prompt the user
    print(f"API Key file not found at {key_path}")
    key = input("Please enter your DeepSeek API Key: ").strip()
    if not key:
        print("Error: API Key is required.")
        sys.exit(1)

    key_path.write_text(key, encoding="utf-8")
    print(f"API Key saved to {key_path}")
    return key


async def main():
    load_dotenv()
    import sys

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="DeepSeek MCP Agent with command line support."
    )
    parser.add_argument(
        "-c", "--command", type=str, help="Execute a single command and exit."
    )
    parser.add_argument(
        "-i", "--stdin", action="store_true", help="Read command from standard input."
    )
    args = parser.parse_args()

    # Determine user input
    user_input = None
    if args.stdin:
        # Read from stdin
        import sys

        user_input = sys.stdin.read().strip()
    elif args.command:
        user_input = args.command.strip()

    # 1. Setup Agent
    api_key = get_api_key()
    agent = DeepSeekMCPAgent(api_key=api_key)

    # 2. Setup Servers
    current_dir = Path(__file__).parent
    servers_dir = current_dir / "servers"

    # Scan for servers
    if servers_dir.exists():
        for item in servers_dir.iterdir():
            if item.is_dir():
                skill_path = item / "SKILL.md"
                server_path = item / "server.py"

                if skill_path.exists() and server_path.exists():
                    print(f"Loading server: {item.name}")
                    agent.add_server(
                        name=item.name,
                        skill_md_path=skill_path,
                        command=sys.executable,
                        args=[str(server_path)],
                    )

    # 3. Decide mode
    if user_input is None:
        # Interactive mode
        try:
            await agent.chat_loop()
        except KeyboardInterrupt:
            pass
    else:
        # Command mode: execute the command using coder skill
        # Ensure coder skill is loaded
        coder_loaded = False
        for skill in agent.skills:
            if skill.config.name == "coder":
                if not skill.loaded:
                    # Load coder skill
                    await agent.call_tool("skill_coder", {})
                coder_loaded = True
                break

        if not coder_loaded:
            print("Error: coder skill not found. Cannot execute command.")
            sys.exit(1)

        # Execute the command via run_terminal_command
        result = await agent.call_tool("run_terminal_command", {"command": user_input})
        print(result)
        # Cleanup
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
