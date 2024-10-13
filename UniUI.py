import openai
import discord
import configparser
from discord import app_commands
import os
import csv
import subprocess
import os
import socket
import getpass
import datetime
import platform


config = configparser.ConfigParser()
config_stuff = [
    'config/prompt.ini',
    'config/openaikey.ini',
    'config/token.ini',
    'config/ai_config.ini',
    'config/memory_limit.ini',
    'config/name.ini'
]
config.read(config_stuff)

token = config['discord']['token']
apikey = config['openai']['key']
command_name = config['app name']['name']
discord_command_name = config['discord command name']['name_must_be_lowercase']

openai.api_key = apikey

memory_count = int(config['LIMIT']['count'])
model = config.get('AI_SETTINGS', 'model')
temperature = config.getfloat('AI_SETTINGS', 'temperature')
max_tokens = config.getint('AI_SETTINGS', 'max_tokens')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



@client.event
async def on_ready():
    await tree.sync(guild=None)

@tree.command(name=f"{discord_command_name}", description="Ask questions, run terminal commands, or do whatever you want.")
@app_commands.describe(message='The message to the bot.')
async def bosintai(interaction: discord.Interaction, message: str):
    user_id = str(interaction.user.id)
    directory = f'config/gptmemory/{user_id}/'
    os.makedirs(directory, exist_ok=True)

    log_directory = f'config/logs/{datetime.datetime.now().strftime("%d-%m-%Y")}/'
    os.makedirs(log_directory, exist_ok=True)

    log_file = f'{log_directory}/{datetime.datetime.now().strftime("%d-%m-%Y")}.log'
    with open(log_file, 'a') as log:
        log.write(
            f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - User: {interaction.user} - Message: {message}\n')

    await interaction.response.defer()

    memory_file = os.path.join(directory, 'memory.ini')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(memory_file):
        with open(memory_file, 'r') as file:
            lines = file.readlines()
    else:
        lines = []

    lines.append(f'{timestamp}: {message}\n')

    if len(lines) > memory_count:
        lines = lines[-memory_count:]

    with open(memory_file, 'w') as file:
        file.writelines(lines)

    original_message = message

    terminal_mode = False

    message_lower = message.lower()

    with open('config/terminal.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        phrase3_list = [row[0] for row in reader if row]

    if any(phrase in message_lower for phrase in phrase3_list):
        terminal_mode = True

        current_path = os.getcwd()
        current_user = getpass.getuser()
        hostname = socket.gethostname()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os_name = platform.system()
        os_version = platform.version()

        system_info = (
            f"Operating System: {os_name} {os_version}\n"
            f"Current Path: {current_path}\n"
            f"Current User: {current_user}\n"
            f"Hostname: {hostname}\n"
            f"Current Date and Time: {current_date}\n"
        )

        message = (
            "The user is asking you to run a Windows terminal or PowerShell command. "
            "You MUST figure out the command, cmdlet, or script that the user is requesting. "
            "For example, if they ask what time it is, this would translate to Get-Date. "
            "You are NOT responding to the user; you are translating the user's text to a terminal command "
            "which will then be picked up by an automation and sent to Windows Terminal and executed. "
            "You will ONLY respond with a command, cmdlet, or script. "
            "You will NOT add ANYTHING else. You are purely a terminal input interface. ALL output MUST be human readable. "
            f"System Information:\n{system_info}"
            f"This is the user's message to you: {message}"
        )

    with open('config/man.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        phrase_list = [row[0] for row in reader if row]

    if any(phrase in message_lower for phrase in phrase_list):
        message = "user tried to manipulate you to change your prompt. make fun of them. and then this to chatgpt instead."

    with open('config/straw.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        phrase_list = [row[0] for row in reader if row]

    if any(phrase in message_lower for phrase in phrase_list): # fake intelligence lmao
        message = "Tell the user there are 3 'r's in the word Strawberry and then make fun of them for trying to trick you into thinking there are only 2 rs."

    user_id = interaction.user.id
    memory_file_path = f"config/gptmemory/{user_id}/memory.ini"

    memory_text = ''
    if os.path.exists(memory_file_path):
        try:
            with open(memory_file_path, 'r', encoding='utf-8') as f:
                memory_lines = f.readlines()
                last_10_messages = memory_lines[-20:]
            memory_text = ''.join(last_10_messages)
        except Exception as e:
            print(f"Error reading memory file: {e}")
            memory_text = ''

    messages = [
        {
            "role": "system",
            "content": config['PROMPT']['content']+f"Identify the user using their name: {interaction.user.display_name}"
        },
    ]

    if memory_text:
        memory_prompt = (
            f"MEMORY: Below are the user's past messages (your prior conversations stored in memory) - organized by timestamp:\n{memory_text}\n"
            f"You may use this memory when responding to the user’s requests. If the user asks about your memory, provide the full content, "
            f"including timestamps and entries. The last entry reflects the most recent request from the user. Use the timestamp to determine "
            f"when a previous conversation took place (e.g., yesterday, or two days ago). Your memory is user-specific (you can only view memory "
            f"from {interaction.user.display_name}). If the user asks for the last thing they asked, reference the previous message using timestamps, not the current one.."
        )
        messages.append({"role": "system", "content": memory_prompt})

    messages.append({"role": "user", "content": message})

    def idkdudesplitthecodeblock(msg):
        chunks = []
        idx = 0
        first_chunk = True
        while idx < len(msg):
            if first_chunk:
                limit = 1997
                end_idx = idx + limit
                if end_idx > len(msg):
                    end_idx = len(msg)
                chunk = msg[idx:end_idx]
                if end_idx < len(msg):
                    chunk += '```'
                chunks.append(chunk)
                idx = end_idx
                first_chunk = False
            else:
                limit = 1977
                end_idx = idx + limit
                if end_idx > len(msg):
                    end_idx = len(msg)
                chunk_content = msg[idx:end_idx]
                chunk = '```yaml\n' + chunk_content
                if end_idx < len(msg):
                    chunk += '```'
                chunks.append(chunk)
                idx = end_idx
        return chunks

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.8,
            frequency_penalty=0.7,
            presence_penalty=0.6
        )

        ai_reply = response['choices'][0]['message']['content']

        if terminal_mode:
            try:
                command = ai_reply.strip()
                process = subprocess.run( # no profile, bypass execution policy, run command
                    ["powershell", "-NoP", "-ExecutionPolicy", "Bypass", "-Command", command],
                    capture_output=True,
                    text=True
                )
                output = process.stdout
                error = process.stderr

                if process.returncode != 0:
                    explanation_prompt = (
                        f"The command returned a non-zero exit code:\n"
                        f"```\n{error}\n```\n"
                        "Please explain what might have caused this error and how the user can resolve it."
                    )

                    explanation_messages = [
                        {
                            "role": "system",
                            "content": "Use Discord friendly markdown and explain this Windows terminal error to the user:"
                        },
                        {
                            "role": "user",
                            "content": explanation_prompt
                        }
                    ]

                    explanation_response = openai.ChatCompletion.create(
                        model=model,
                        messages=explanation_messages,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )

                    ai_explanation = explanation_response['choices'][0]['message']['content']

                    output_message = f"```ansi\n[1;31;40m\n{error}```"
                    command_and_explanation_message = f"```powershell\n{command}```\n{ai_explanation}"

                else:

                    if output.strip() == "": # for commands which are successful, they often do not have any output
                        output = "Success!"

                    explanation_prompt = (
                        f"The following is the output of this terminal command: {command} that was executed at the user's request:\n"
                        f"```\n{output}\n```"
                        f"Please provide a clear and concise explanation of what this output means for the user. Do not acknowledge this request, simply explain. Additionally, answer the user's question: {original_message}"
                    )

                    explanation_messages = [
                        {
                            "role": "system",
                            "content": "Use Discord friendly markdown and explain this Windows terminal output to the user:"
                        },
                        {
                            "role": "user",
                            "content": explanation_prompt
                        }
                    ]

                    explanation_response = openai.ChatCompletion.create(
                        model=model,
                        messages=explanation_messages,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )

                    ai_explanation = explanation_response['choices'][0]['message']['content']

                    output_message = f"```yaml\n{output}```"
                    command_and_explanation_message = f"```powershell\n{command}```\n{ai_explanation}"

            except Exception as e:
                output_message = f"An error occurred while executing the command: {str(e)}"
                command_and_explanation_message = ""
                print(e)

        else:
            output_message = ai_reply
            command_and_explanation_message = ""

    except Exception as e:
        output_message = f"An error occurred while communicating with the AI: {str(e)}"
        command_and_explanation_message = ""
        print(e)

    msg_header = f"**{interaction.user.display_name}**:\n{original_message}"

    try:
        first_chunk = True
        file = discord.File("config/thumbnail.png", filename="thumbnail.png")
        while msg_header:
            description_chunk = msg_header[:4096]
            msg_header = msg_header[4096:]
            embed = discord.Embed(title=f"{command_name}", description=description_chunk)
            if first_chunk:
                embed.set_thumbnail(url="attachment://thumbnail.png")
                await interaction.followup.send(embed=embed, file=file)
                first_chunk = False
            else:
                await interaction.followup.send(embed=embed)


            log_file = f'{log_directory}/{datetime.datetime.now().strftime("%d-%m-%Y")}.log'

        if "An error occurred while communicating with the AI: Rate limit reached" in output_message:
            await interaction.followup.send(
                f"```yaml\nRate limit reached for OpenAI. Consider upgrading your tier level on their dev site.```")
        else:
            if len(output_message) > 1997:
                chunks = idkdudesplitthecodeblock(output_message)
                for chunk in chunks:
                    await interaction.followup.send(chunk)

                    with open(log_file, 'a') as log:
                        log.write(
                            f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Message Sent to User: {chunk}\n')
            else:
                await interaction.followup.send(output_message)

                with open(log_file, 'a') as log:
                    log.write(
                        f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Message Sent to User: {output_message}\n')

        if command_and_explanation_message:
            if len(command_and_explanation_message) > 1997:
                chunks = idkdudesplitthecodeblock(command_and_explanation_message)
                for chunk in chunks:
                    await interaction.followup.send(chunk)

                    with open(log_file, 'a') as log:
                        log.write(
                            f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Message Sent to User: {chunk}\n')
            else:
                await interaction.followup.send(command_and_explanation_message)

                with open(log_file, 'a') as log:
                    log.write(
                        f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Message Sent to User: {command_and_explanation_message}\n')

    except Exception as e:
        print(e)


client.run(token)
