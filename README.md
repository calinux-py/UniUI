# UniUI AI Discord Bot

UniUI is an intelligent Discord bot that can communicate, store memories, and even execute terminal commands on Windows.

[<img src="https://github.com/calinux-py/UniUI/blob/main/config/Screenshot%202024-10-10%20204138.png?raw=true" alt="Ephemeral Logo" width="63%">](https://github.com/calinux-py/Ephemeral)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
  - [config/prompt.ini](#configpromptini)
  - [config/openaikey.ini](#configopenaikeyini)
  - [config/token.ini](#configtokenini)
  - [config/ai_config.ini](#configai_configini)
  - [config/memory_limit.ini](#configmemory_limitini)
  - [config/name.ini](#confignameini)
  - [config/terminal.csv](#configterminalcsv)
  - [config/man.csv](#configmancsv)
  - [config/straw.csv](#configstrawcsv)
- [Usage](#usage)
- [Logging](#logging)
- [License](#license)

## About

UniUI is a Discord bot that integrates with OpenAI's GPT models to generate interactive responses to user messages, while maintaining a per-user memory of past interactions. It detects certain phrases to switch into a terminal mode, where it translates user requests into Windows Cmd/PowerShell commands, executes them on the server, and returns the output or explanations back to the user. Additionally, the bot includes safeguards against prompt manipulation attempts and provides witty responses when such attempts are detected.

## Features

- **AI Interaction**: Engage in conversations with the bot, powered by OpenAI's GPT models.
- **Terminal Command Execution**: Translate user messages into Windows terminal or PowerShell commands and execute them.
- **User-Specific Memory**: Maintain a memory log for each user to provide context in conversations.
- **Customizable Prompts**: Modify the system prompt to change the bot's behavior.
- **Command Logging**: Logs all user interactions and bot responses.
- **Configurable AI Settings**: Adjust model parameters like temperature and max tokens.
- **User Friendly**: Once the bot is running in Python, you won't need to modify the code. Simply adjust the .ini and .csv to your preferences.

## Prerequisites

- Python 3.7 or higher
- Discord bot token
- OpenAI API key
- Required Python packages:
  - `openai`
  - `discord`

## Installation

1. **Clone the Repository**

   ```cmd
   git clone https://github.com/calinux-py/UniUI.git
   cd UniUI
   ```

2. **Install Required Packages**

   ```cmd
   pip install -r requirements.txt
   ```

3. **Set Up Configuration Files**

   Edit the following configuration files inside a `config` directory. See the [Configuration](#configuration) section for details.

   - `config/prompt.ini`
   - `config/openaikey.ini`
   - `config/token.ini`
   - `config/ai_config.ini`
   - `config/memory_limit.ini`
   - `config/name.ini`
   - `config/terminal.csv`
   - `config/man.csv`
   - `config/straw.csv`

4. **Run the Bot**

   ```cmd
   python UniUI.py
   ```

## Configuration

The bot relies on several configuration files located in the `config` directory. Here's what each file does:

### config/prompt.ini

Defines the system prompt that sets the initial behavior of the AI.

```ini
[PROMPT]
content = Your custom system prompt here.
```

### config/openaikey.ini

Stores your OpenAI API key.

```ini
[openai]
key = YOUR_OPENAI_API_KEY
```

### config/token.ini

Contains your Discord bot token.

```ini
[discord]
token = YOUR_DISCORD_BOT_TOKEN
```

### config/ai_config.ini

Configures the AI model settings.

```ini
[AI_SETTINGS]
model = gpt-3.5-turbo
temperature = 0.7
max_tokens = 150
```

### config/memory_limit.ini

Sets the number of past messages to retain in the user's memory log.

```ini
[LIMIT]
count = 20
```

### config/name.ini

Specifies the bot's display name and Discord command name.

```ini
[app name]
name = UniUI

[discord command name]
name_must_be_lowercase = uniui
```

### config/terminal.csv

A CSV file containing phrases that trigger terminal command execution mode.

```
run command
execute
terminal
```

### config/man.csv

Contains phrases that the bot uses to detect manipulation attempts.

```
change prompt
ignore previous
alter behavior
```

### config/straw.csv

Includes phrases to trigger a specific Easter egg response about the word "Strawberry."

```
how many rs in strawberry
strawberry has how many rs
```

## Usage

Once the bot is running, you can interact with it on your Discord server using the slash command defined in `config/name.ini`.

### Basic Interaction

- **Command Format**: `/uniui <message>`
- **Example**:

  ```
  /uniui Hello, how are you?
  ```

### Terminal Command Execution

If your message includes any phrases from `config/terminal.csv`, the bot will attempt to translate your request into a Windows terminal command, execute it, and provide the output.

- **Example**:

  ```
  /uniui Using the terminal, list all files in the current directory.
  ```

### Memory Recall

The bot maintains a memory of your past interactions, limited by the count specified in `config/memory_limit.ini`. It uses this memory to provide context in conversations.

## Logging

- **Logs Directory**: `config/logs/`
- **Memory Files**: `config/gptmemory/<user_id>/memory.ini`

All interactions are logged with timestamps, user IDs, and messages.

## License

MIT
