# Pi Coding Agent — Combined Documentation

> Combined from `official-docs/` for NotebookLM / LLM upload.
> Generated: 2026-10-03

---


<!-- ============================================================ -->
<!-- SOURCE: README.md -->
<!-- ============================================================ -->

# Pi Documentation (Local Mirror)

Mirrored from <https://pi.dev/docs/latest> on 2026-10-03 — source: [`earendil-works/pi`](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/docs) (formerly `badlogic/pi-mono`).

Organized to match the official navigation in `docs.json`. Re-sync with `uv run python docs/pi-docs/sync_official_docs.py`.

## Get Started — [`01-get-started/`](01-get-started/)

- [Overview](01-get-started/01-index.md) — `index.md`
- [Quickstart](01-get-started/02-quickstart.md) — `quickstart.md`
- [How Pi Works](01-get-started/03-how-pi-works.md) — `how-pi-works.md`

## Run Pi — [`02-run-pi/`](02-run-pi/)

- [Use Pi in the Terminal](02-run-pi/01-usage.md) — `usage.md`
- [Choose a Model](02-run-pi/02-models.md) — `models.md`
- [Manage Sessions and Context](02-run-pi/03-sessions.md) — `sessions.md`
- [Run Pi Safely](02-run-pi/04-security.md) — `security.md`
- [Isolate Pi](02-run-pi/05-containerization.md) — `containerization.md`
- [Run Local Models](02-run-pi/06-llama-cpp.md) — `llama-cpp.md`
- [Configure Your Terminal](02-run-pi/07-terminal-setup.md) — `terminal-setup.md`
- [Configure Shell Commands](02-run-pi/08-shell-aliases.md) — `shell-aliases.md`
- [Run Pi in tmux](02-run-pi/09-tmux.md) — `tmux.md`
- [Run Pi on Windows](02-run-pi/10-windows.md) — `windows.md`
- [Run Pi on Android](02-run-pi/11-termux.md) — `termux.md`

## Customize Pi — [`03-customize-pi/`](03-customize-pi/)

- [Configure Pi](03-customize-pi/01-configuration.md) — `configuration.md`
- [Create Prompt Templates](03-customize-pi/02-prompt-templates.md) — `prompt-templates.md`
- [Add Skills](03-customize-pi/03-skills.md) — `skills.md`
- [Create Themes](03-customize-pi/04-themes.md) — `themes.md`
- [Use Pi Packages](03-customize-pi/05-packages.md) — `packages.md`
- [Connect MCP Servers](03-customize-pi/06-mcp.md) — `mcp.md`

## Build on Pi — [`04-build-on-pi/`](04-build-on-pi/)

- [Build Extensions](04-build-on-pi/01-extensions.md) — `extensions.md`
- [Add Custom Providers](04-build-on-pi/02-custom-provider.md) — `custom-provider.md`
- [Route with Virtual Models](04-build-on-pi/03-virtual-models.md) — `virtual-models.md`
- [Build Terminal UI Components](04-build-on-pi/04-tui.md) — `tui.md`
- [Integrate with the CLI](04-build-on-pi/05-cli-integration.md) — `cli-integration.md`
- [Use the SDK](04-build-on-pi/06-sdk.md) — `sdk.md`

## Reference — [`05-reference/`](05-reference/)

- [CLI](05-reference/01-cli.md) — `cli.md`
- [Codemode](05-reference/02-codemode.md) — `codemode.md`
- [Slash Commands](05-reference/03-slash-commands.md) — `slash-commands.md`
- [Settings](05-reference/04-settings.md) — `settings.md`
- [Environment Variables](05-reference/05-environment-variables.md) — `environment-variables.md`
- [Keybindings](05-reference/06-keybindings.md) — `keybindings.md`
- [Providers](05-reference/07-providers.md) — `providers.md`
- [Session File Format](05-reference/08-session-format.md) — `session-format.md`
- [Compaction and Branch Summaries](05-reference/09-compaction.md) — `compaction.md`
- [JSON Event Stream](05-reference/10-json.md) — `json.md`
- [RPC Protocol](05-reference/11-rpc.md) — `rpc.md`
- [RPC Commands](05-reference/12-rpc-commands.md) — `rpc-commands.md`
- [RPC Extension UI](05-reference/13-rpc-extension-ui.md) — `rpc-extension-ui.md`
- [Message Types](05-reference/14-message-types.md) — `message-types.md`


<!-- ============================================================ -->
<!-- SOURCE: 01-get-started/01-index.md -->
<!-- ============================================================ -->

# Pi

Pi is an extensible AI agent that works from your terminal. Give it a goal and a working folder, and it can inspect files, run commands, edit content, and work through multi-step tasks.

Use Pi for software development, research notes, writing projects, data files, or hobby work. You can use Pi as is, prompt it to adapt itself to your workflow, or build other applications powered by Pi using the SDK.

## Start using Pi

New to Pi? Follow the [Quickstart](../01-get-started/02-quickstart.md) to install Pi, connect a model, and complete your first task.

If Pi is already installed, choose what you want to do:

- [Use Pi interactively](../02-run-pi/01-usage.md) to add files, run commands, direct ongoing work, and export results.
- [Choose a model](../02-run-pi/02-models.md) or connect a subscription, API key, local model, or compatible endpoint.
- [Continue or branch a session](../02-run-pi/03-sessions.md) to resume work or explore another approach without losing history.
- [Configure Pi](../03-customize-pi/01-configuration.md) for your preferences, working folders, instructions, and reusable resources.
- [Understand how Pi works](../01-get-started/03-how-pi-works.md), including tools, context, sessions, and the agent loop.

## Customize Pi

Pi can reuse prompts, load specialized instructions, add executable integrations, change its terminal interface, connect model services, and distribute these resources as packages.
Use the [Quickstart customization chooser](../01-get-started/02-quickstart.md#choose-how-to-customize-pi) to select the smallest mechanism that meets your need.

## Automate or embed Pi

- Use [print mode](../05-reference/01-cli.md#invocation-and-output) for one-off and scripted tasks.
- Use [JSON event stream mode](../05-reference/10-json.md) to consume structured events from one run.
- Use [RPC mode](../05-reference/11-rpc.md) to control a separate Pi process.
- Use the [TypeScript SDK](../04-build-on-pi/06-sdk.md) to run Pi inside an application.

## Find reference and setup information

Use the reference pages to look up [CLI options](../05-reference/01-cli.md), [settings](../05-reference/04-settings.md), [providers](../05-reference/07-providers.md), [keybindings](../05-reference/06-keybindings.md), and [environment variables](../05-reference/05-environment-variables.md).

For platform-specific help, see [Terminal Setup](../02-run-pi/07-terminal-setup.md), [Windows](../02-run-pi/10-windows.md), [tmux](../02-run-pi/09-tmux.md), [Termux on Android](../02-run-pi/11-termux.md), or [Containerization](../02-run-pi/05-containerization.md).

## Work safely

Pi's tools and extensions run with the permissions of the Pi process. Project trust controls which project resources Pi loads, but it does not sandbox tool calls. Review [Security](../02-run-pi/04-security.md) before using untrusted files, repositories, extensions, or unattended automation.


<!-- ============================================================ -->
<!-- SOURCE: 01-get-started/02-quickstart.md -->
<!-- ============================================================ -->

# Quickstart

Pi runs in your terminal and works with files on your machine. To use it, you need access to a model through a supported provider. This can be a subscription, an API key, or a local model.

For native Windows setup, read [Windows Setup](../02-run-pi/10-windows.md). For Android, read [Termux Setup](../02-run-pi/11-termux.md).

## 1. Install Pi

On macOS or Linux, you can use the installer:

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

The installer pins all dependencies and updates Pi with `pi update`. Alternatively, install Pi from npm, which does not pin transitive dependencies. This requires Node.js 22.19 or newer:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

Pi does not require dependency lifecycle scripts for a normal npm installation.

With Nix on macOS or Linux, install the latest release from Pi's flake. Nix builds Pi from source:

```bash
nix profile add github:earendil-works/pi/stable
```

Older Nix versions use `nix profile install` instead. Update with `nix profile upgrade pi`; `pi update` cannot update a Nix installation. To pin a release, use a tag such as `github:earendil-works/pi/v1.0.0`.

Verify the installation:

```bash
pi --version
```

## 2. Start Pi

Change to the folder you want Pi to work with, then start it:

```bash
cd /path/to/folder
pi
```

The working folder helps Pi discover relevant files, instructions, and configuration. Pi also uses it to group saved sessions.

<p align="center"><img src="../images/interactive-mode.png" alt="Pi running in a terminal with a conversation, input editor, and status footer" width="750"></p>

The interface shows your conversation, an editor for prompts and commands, and a footer with the current folder, model, and session status. See [Use Pi in the terminal](../02-run-pi/01-usage.md) to learn how to add files, run commands, direct ongoing work, and manage results.

## 3. Choose a model

A **model** generates Pi's responses. A **provider** is the service or account Pi uses to access that model.

In Pi, run:

```text
/login
```

Choose a provider, then follow the prompts to use a subscription or store an API key. Run `/model` afterward if you want to select a different available model.

See [Choose a model and provider](../02-run-pi/02-models.md) for supported providers, environment-variable authentication, local models, and custom endpoints.

## 4. Give Pi a task

Pi shows each file read, search, command, and edit it performs. It does not ask before every tool call.

Enter a task that matches your work, for example:

```text
Summarize @meeting-notes.md and save the action items to action-items.md.
```

```text
Explain how this repository is structured and how to run its checks.
```

```text
Compare @previous.csv with @current.csv and summarize the important changes.
```

Type `@` in the editor to search for a file instead of entering its full path. When Pi finishes, review its response and any changed files. Use version control or backups for important work. For untrusted or unattended work, use a container or another sandbox. See [Security](../02-run-pi/04-security.md).

## Continue later

Pi saves sessions automatically. Exit Pi, then resume the most recent session for the same working folder with:

```bash
pi --continue
```

Use `/resume` to choose another saved session. See [Continue or branch a session](../02-run-pi/03-sessions.md) for session naming, branching, compaction, export, and sharing.

## Next steps

- [Use Pi interactively](../02-run-pi/01-usage.md) to learn input, commands, shortcuts, and queued messages.
- [Add instructions](../03-customize-pi/01-configuration.md#context-files) that Pi should follow whenever it works in a folder.
- [Choose a model and provider](../02-run-pi/02-models.md).

### Choose how to customize Pi

Start with the least powerful mechanism that meets your need:

| Need | Start with |
|---|---|
| Give Pi persistent instructions for a folder | [`AGENTS.md`](../03-customize-pi/01-configuration.md#context-files) |
| Reuse a prompt from the `/` menu | [Prompt template](../03-customize-pi/02-prompt-templates.md) |
| Add task-specific instructions and supporting files | [Skill](../03-customize-pi/03-skills.md) |
| Add executable tools, commands, or event handlers | [Extension](../04-build-on-pi/01-extensions.md) |
| Build a custom terminal component | [Terminal UI](../04-build-on-pi/04-tui.md) |
| Connect an unsupported model service | [Custom provider](../04-build-on-pi/02-custom-provider.md) |
| Install or distribute several resources | [Pi package](../03-customize-pi/05-packages.md) |

## Uninstall Pi

If you installed Pi with npm, run:

```bash
npm uninstall -g @earendil-works/pi-coding-agent
```

If you used the installer, run it again and choose **Uninstall Pi**:

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

If you installed Pi with Nix, run:

```bash
nix profile remove pi
```

None of these methods removes configuration, credentials, sessions, or installed Pi packages from `~/.pi/agent/`.


<!-- ============================================================ -->
<!-- SOURCE: 01-get-started/03-how-pi-works.md -->
<!-- ============================================================ -->

# How Pi Works

Pi coordinates model requests, tool execution, context assembly, and session storage. A session is Pi's record of a conversation, including messages, tool calls and results, model changes, compactions, and other events.

Messages and events in a session form a tree. Each path through that tree is a branch. The branch ending at the current entry is the active branch and supplies the history for the next model request.

## Agent loop

A submitted message is added to the active branch. Pi builds a model request from the system prompt, active branch, available tools, and model settings, then sends it through the selected provider.

The provider streams an assistant response, which can contain text and tool calls. Pi records the response, executes each tool call, and records the results. That completes one turn. If tool results or queued messages require another model request, Pi starts another turn. Otherwise, the run ends.

Steering messages enter after the current assistant turn. Follow-up messages enter after the agent has finished its pending work. Aborting stops the current run and returns queued messages to the editor.

## Context

The active branch supplies conversation history. Pi converts its session entries into model-compatible user, assistant, and tool-result messages.

Pi builds the system prompt from its base instructions and discovered context files. The request also carries tool definitions and skill descriptions.

Full skill instructions are loaded on demand. Extensions can add instructions or transform context.

Prompt templates expand editor input before it becomes a user message. Selected files, images, pasted text, and shell output can become message content.

## Sessions

Persistent sessions are JSONL files. Each tree entry has an ID and refers to its parent. The current entry identifies the active branch.

Continuing from an earlier entry creates another branch in the same file. Forking and cloning copy selected history into a new session file.

Model context is reconstructed from the active branch. Compaction inserts a summary entry that replaces older messages in subsequent model requests. The original entries remain in the session tree.

## Interfaces

Interactive mode renders session and agent events in the terminal. Print mode runs a prompt and writes the final response. JSON mode writes agent events as JSONL.

RPC mode accepts JSONL commands on stdin and writes responses and events to stdout. The TypeScript SDK creates and controls agent sessions in process.

All interfaces use the same agent and session mechanisms.

## Extensions and resources

Extensions are TypeScript modules loaded into the Pi process. Their factory functions register tools, commands, shortcuts, providers, event handlers, renderers, and terminal UI.

Skills provide on-demand instructions and supporting files. Prompt templates provide reusable message text. Themes provide terminal colors. Pi packages distribute these resources through npm or git.

## Trust and permissions

Pi resolves project trust before loading project settings and resources. After the trust decision and project-resource loading, Pi loads context files. Enabled tools use the operating-system permissions of the Pi process. Extensions execute inside that process.


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/01-usage.md -->
<!-- ============================================================ -->

# Use Pi in the terminal

Run `pi` from the folder you want to work in. Pi uses that folder to discover files, instructions, and configuration, and to group saved sessions. If you have not installed Pi or chosen a model yet, follow the [Quickstart](../01-get-started/02-quickstart.md).

Pi may ask whether you trust the working folder before loading its project resources. See [Project trust](../02-run-pi/04-security.md#understand-project-trust).

<p align="center"><img src="../images/interactive-mode.png" alt="Pi interactive mode showing a conversation, editor, and status information" width="750"></p>

The transcript shows your prompts, Pi's responses, tool calls, results, and errors. You write prompts and commands in the editor. The footer shows the current folder, session, model, context usage, and accumulated usage and cost.

## Enter a prompt

Type a request and press `Enter` to send it. Use `Shift+Enter` to add a line, or press `Ctrl+G` to work on a longer prompt in your configured external editor.

To include files or images:

- Type `@` to search for a file and add it to your prompt.
- Press `Tab` to complete a path.
- Paste an image or drag it into a compatible terminal.

## Follow Pi's work

Pi shows each tool call and result while it works. Press `Ctrl+O` to expand or collapse tool output. Press `Ctrl+T` to show or hide thinking blocks.

The startup header lists the instructions and resources Pi loaded. The editor border indicates the current thinking level. The footer updates as the model uses context and reports usage.

Pi does not ask before every tool call. Review commands and changed files, and use a sandbox for untrusted or unattended work. See [Security](../02-run-pi/04-security.md).

## Change direction

You can send more input while Pi is working:

| What you want | Action |
|---|---|
| Adjust the current task | Type a message and press `Enter` |
| Add work after the current task | Type a message and press `Alt+Enter` |
| Return queued messages to the editor | Press `Alt+Up` |
| Stop the current task | Press `Escape` |

A message sent with `Enter` waits until the current response and its tool calls finish, then guides the next response. A follow-up sent with `Alt+Enter` waits until Pi finishes the current task. Aborting returns queued messages to the editor.

Windows Terminal reserves some Alt shortcuts. See [Terminal Setup](../02-run-pi/07-terminal-setup.md) for the Windows alternatives.

## Change the model or settings

Type `/` to search the available commands. The commands you will use most often are:

- `/model` selects a model. Press `Ctrl+L` to open the same selector.
- `/thinking` selects how much reasoning the current model uses. Press `Shift+Tab` to cycle through supported levels.
- `/login` and `/logout` manage provider access.
- `/settings` changes common preferences.

Prompt templates, skills, and extensions can add more commands to the same menu. See [Choose a Model](../02-run-pi/02-models.md), [Configuration](../03-customize-pi/01-configuration.md), or the complete [Slash Commands reference](../05-reference/03-slash-commands.md).

## Continue or start over

Pi saves sessions automatically unless session persistence is disabled.

- `/new` starts a new session.
- `/resume` opens another saved session.
- `/name` gives the current session a recognizable name.
- `/session` shows its file, ID, message count, token usage, and cost.

Use `/tree`, `/fork`, or `/clone` when you want to explore another approach without losing existing work. Use `/compact` to reduce the conversation history sent to the model. See [Sessions and Context](../02-run-pi/03-sessions.md) for these workflows.

After leaving Pi, run `pi --continue` from the same folder to resume its most recent session.

## Run a terminal command

Prefix a command with `!` to run it and include its output in the conversation:

```text
!git status
```

Use `!!` when you want to run a command without sending its output to the model.

## Copy, export, or share results

Press `Ctrl+X` or run `/copy` to copy the last assistant response. Use `/export` to save the session as HTML or JSONL.

Use `/share` to upload the session and get a viewer link. With Radius authentication, the artifact is visible to your Radius organization. Otherwise, Pi creates a private GitHub gist through the GitHub CLI. Review the session first because it can contain prompts, tool output, file contents, and credentials exposed during the conversation.

## Adjust the terminal

Fullscreen mode, the default, keeps the editor and status area fixed while the transcript scrolls within the terminal window. Regular mode uses the terminal's normal scrollback. Choose a mode through `/settings` or `--tui-mode`.

Terminal support for mouse input, keyboard shortcuts, and inline images varies. See [Terminal Setup](../02-run-pi/07-terminal-setup.md) for platform-specific configuration and [Keybindings](../05-reference/06-keybindings.md) for every configurable shortcut. Run `/hotkeys` to inspect the shortcuts active in your current session.

## Collect diagnostic information

When troubleshooting terminal rendering or conversation state, run `/debug`. Pi writes the rendered terminal lines and current session messages to `pi-debug.log` in your [agent directory](../03-customize-pi/01-configuration.md#agent-directory).

Review this file before sharing it. It can contain prompts, model responses, tool output, file contents, and terminal data.


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/02-models.md -->
<!-- ============================================================ -->

# Choose a Model

For a built-in provider, start with `/login`, then choose a model with `/model`. Use custom model configuration only when Pi does not already include the provider or endpoint you need.

## Choose a connection

| What you have | Recommended setup |
|---|---|
| A supported subscription | Sign in through `/login` |
| A provider API key | Store it through `/login` or set its environment variable |
| A local GGUF model | Connect Pi to the llama.cpp router |
| An OpenAI-, Anthropic-, or Google-compatible endpoint | Add it to `models.json` |
| A provider with a custom protocol or authentication flow | Build or install a provider extension |

Browse the [model catalog](https://pi.dev/models) for current providers, model IDs, capabilities, context limits, and pricing. Pi starts with its bundled catalog and can overlay newer catalog data from pi.dev. Cached catalog data remains available offline; run `pi update --models` to force a refresh.

## Authenticate

Run `/login` and select a provider. Pi stores credentials in [`auth.json`](../03-customize-pi/01-configuration.md#agent-directory). Run `/logout` to remove stored credentials for a provider.

You can instead provide an API key through the provider's environment variable. This is useful in CI and other environments where Pi should not write credentials. [Providers](../05-reference/07-providers.md) lists the variables and provider-specific setup.

When several credential sources are configured, Pi uses a runtime `--api-key` first, then a stored `auth.json` credential, an `apiKey` from `models.json`, and finally the provider's environment variables or ambient cloud credentials. Provider extensions can define their own authentication behavior.

Keep `auth.json` and any credential commands private. Project settings and extensions can execute inside the Pi process after you trust a project. Review [Security](../02-run-pi/04-security.md) before loading configuration from an untrusted directory.

## Select a model

Run `/model` to search available models. The picker shows models whose providers have usable authentication. Press `Ctrl+S` on a model to save it as the default for new sessions.

Run `/thinking` to select the thinking level for the current model. Press `Ctrl+S` there to save the startup level. Pi limits the choices to levels supported by the selected model.

`Ctrl+P` cycles through available models. Use `/scoped-models` to control that cycle and save the selection, or configure model patterns through [Settings](../05-reference/04-settings.md#model-cycling).

A session records model and thinking-level changes. Resuming the session restores them without changing defaults for new sessions.

## Connect local models

Pi integrates directly with the llama.cpp router. The router discovers GGUF files and loads models on demand. Pi's `/llama` command manages the router, while `/model` selects one of its loaded models.

Follow [Local Models with llama.cpp](../02-run-pi/06-llama-cpp.md) for server startup, model layout, downloads, and connection troubleshooting.

For Ollama, LM Studio, vLLM, SGLang, and other compatible servers, [configure a compatible endpoint](#configure-a-compatible-endpoint) in `models.json`.

## Configure a compatible endpoint

Use [`models.json`](../03-customize-pi/01-configuration.md#agent-directory) when an endpoint speaks an API Pi already supports. This includes most Ollama, LM Studio, vLLM, SGLang, and proxy deployments.

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [
        { "id": "qwen2.5-coder:7b" }
      ]
    }
  }
}
```

The dummy key makes the model available to Pi; Ollama ignores it. For an authenticated endpoint, `apiKey` and header values can use `$NAME` or `${NAME}` environment interpolation, a literal value, or a leading `!command`. Commands in `models.json` run at request time and are not cached by Pi.

Opening `/model` reloads the file. A `models` entry adds or replaces a model with the same ID on that provider. Use `modelOverrides` to change metadata for an existing built-in or extension-provided model without replacing the provider's model list. Unknown override IDs are ignored.

### Describe model input and caching

Use `inputLimits.images.resize` to control how Pi encodes new image attachments, `read` results, and tool-result images before storing them in conversation history:

```json
{
  "id": "vision-model",
  "input": ["text", "image"],
  "inputLimits": {
    "images": {
      "resize": {
        "maxWidth": 1568,
        "maxHeight": 1568,
        "maxBytes": 524288,
        "jpegQuality": 75
      }
    }
  }
}
```

`maxBytes` limits the base64-encoded payload. Omitted resize fields use conservative defaults of 2000 by 2000 pixels, 4.5 MiB encoded, and JPEG quality 80. Images are encoded once; changing models does not rewrite historical images. The catalog can also describe hard request limits with `inputLimits.maxRequestBytes`, `images.maxPerMessage`, and `images.maxPerRequest`, but Pi does not yet rewrite or reject history based on them.

<a id="prompt-cache-lifetimes"></a>

Use `promptCache` to declare the provider's best-effort cache lifetime in seconds for the `short` or `long` retention tier:

```json
{ "id": "claude-sonnet-5", "promptCache": { "short": 300, "long": 3600 } }
```

Choose the conservative end of any published range. A model without a lifetime for the active tier is not eligible for cache warming. A `modelOverrides` entry can set `inputLimits` or `promptCache` for a built-in or extension model, including a model accessed through a validated proxy. See [`cacheWarming`](../05-reference/04-settings.md#model-and-thinking).

Compatibility settings should describe verified differences in the endpoint's request or response behavior. Do not enable them based only on an endpoint advertising OpenAI or Anthropic compatibility.

## Use classifier models

Classifier models do not chat. They answer typed questions about JSON state: pick one of several choices, answer yes or no, or give a score, each with probabilities. Pi includes TypeSafe's Jev model from these providers, and Cloudflare's Clef and Clef Flash models from Workers AI:

| Provider | Model IDs | Authentication |
|---|---|---|
| `typesafe` | `jev-latest` | `TYPESAFE_API_KEY` |
| `openrouter` | `typesafe/jev-1.13`, `~typesafe/jev-latest` | `OPENROUTER_API_KEY` or `/login` |
| `cloudflare-workers-ai` | `typesafe/jev`, `@cf/cloudflare/clef`, `@cf/cloudflare/clef-flash` | `CLOUDFLARE_API_KEY` and `CLOUDFLARE_ACCOUNT_ID` |
| `vercel-ai-gateway` | `typesafe-ai/jev` | `AI_GATEWAY_API_KEY` |
| `opencode` | `jev-1.13`, `jev-1.13-free` | `OPENCODE_API_KEY` |

Chat models on a [llama.cpp router](../02-run-pi/06-llama-cpp.md#classification) are also listed as classifier models.

Classifier models do not appear in `/model`. The model reaches them through the [`codemode`](../05-reference/01-cli.md#enable-codemode) tool, which is off unless an MCP server turned it on. Enable it with `"defaultTools": ["+codemode"]` in [settings](../05-reference/04-settings.md#tools). Scripts then list classifier models with `models.getAvailableOfType("classifier")` and call `models.classify(model, { state, questions })`:

```js
const jev = await models.getModelOfType("classifier", "typesafe", "jev-latest");
const result = await models.classify(jev, {
  state: { message: "The change works, thanks." },
  questions: {
    approved: {
      type: "bool",
      instructions: "Does the user approve of the result?",
      criteria: { true: "Approval", false: "No approval" },
    },
  },
});
return result.answers;
```

[Codemode](../05-reference/02-codemode.md#classify) describes the question and answer types.

When the service reports token counts, as all System One services do, `result.usage` carries them with their cost. Pi adds the usage of a script's classifier calls to the `codemode` tool result, so it counts toward the session cost in the footer and `/session`. The cost uses the model's catalog price; models without one, such as TypeSafe's direct `jev-latest`, report tokens at no cost.

Extensions call classifiers through `ctx.modelRegistry.classify()`, without codemode. [Virtual models](../04-build-on-pi/03-virtual-models.md#route-requests) can use them to route requests; see the `jev-router.ts` example.

## Use image models

Image models generate images from a prompt and optional input images. Pi lists OpenRouter's image models, such as `google/gemini-2.5-flash-image` and `black-forest-labs/flux.2-pro`, under the `openrouter` provider; they use the same `OPENROUTER_API_KEY` or `/login` credential as its chat models.

Like classifier models, image models do not appear in `/model`; the model reaches them through the [`codemode`](../05-reference/01-cli.md#enable-codemode) tool. Scripts list them with `models.getAvailableOfType("image")` and call `models.generateImages(model, { input })`. The result's `output` holds base64 image blocks, which `image()` attaches to the `codemode` result so the model sees them:

```js
const painter = await models.getModelOfType("image", "openrouter", "google/gemini-2.5-flash-image");
const result = await models.generateImages(painter, {
  input: [{ type: "text", text: "A red fox in the snow, watercolor" }],
});
if (result.stopReason !== "stop") return result.errorMessage;
for (const block of result.output) if (block.type === "image") image(block);
```

`input` can also contain `{ type: "image", data, mimeType }` blocks to edit or use as references. Pi adds the usage of a script's image calls to the `codemode` tool result, like classifier calls. Generated images are not saved to disk. [Codemode](../05-reference/02-codemode.md#generate-images) describes the full API.

Extensions generate images through `ctx.modelRegistry.generateImages()`, without codemode.

## Add a custom provider

Use an extension when the provider needs custom streaming, model discovery, or authentication behavior. See [Custom Providers](../04-build-on-pi/02-custom-provider.md) for the extension workflow.

## Troubleshooting

### A model does not appear

Confirm that its provider has usable authentication. Custom models can load from `models.json` but remain unavailable in `/model` until Pi can resolve credentials. For llama.cpp, only models currently loaded by the router appear.

### Authentication works in one shell only

Check whether the key came from an environment variable rather than `auth.json`. Environment variables must be present in the process that starts Pi.

### Sign-in opens a browser on a remote machine

Complete the provider's headless authentication flow when available. Some providers let you paste the final redirect URL or authorization code back into Pi. See [Authenticate interactively](../05-reference/07-providers.md#authenticate-interactively).

### A compatible endpoint rejects requests

Check its API type and compatibility settings in `models.json`. The upstream server must support the corresponding request fields and behavior.


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/03-sessions.md -->
<!-- ============================================================ -->

# Sessions and Context

Pi saves a conversation as a session. The active branch of that session supplies conversation history for the next model request. Use session commands to continue work, explore another branch, or reduce the amount of history sent to the model.

## Continue or switch sessions

Pi saves sessions automatically unless you start it with `--no-session`.

```bash
pi --continue
pi --resume
```

`--continue` opens the most recent session for the current working directory. `--resume` opens the session picker. In interactive mode, `/resume` opens the same picker and `/new` starts a new session.

Use `/name` or `--name` to assign a recognizable session name. Run `/session` to verify the current session file, ID, message count, token usage, and cost.

The session picker lets you search, rename, and delete sessions. It can also show paths, change sorting, and limit results to named sessions. See [Keybindings](../05-reference/06-keybindings.md#sessions) for its shortcuts.

## Choose how to branch

Pi stores entries as a tree, so returning to an earlier point does not erase the branch you leave.

| Action | Result | Use it when |
|---|---|---|
| `/tree` | Moves within the current session file | Related alternatives should stay together |
| `/fork` | Creates a new session from an earlier user message | The alternative should become separate work |
| `/clone` | Copies the active branch into a new session | You want a separate copy of the current state |

In `/tree`, select a user message to put its text back in the editor. Edit and submit it to create another branch. Selecting an assistant response or another entry continues after that entry with an empty editor.

When you leave a branch, Pi can summarize it and attach that summary to the branch you enter. This preserves relevant work from the abandoned path without including every message from it.

For the persisted tree and entry types, see [Session Format](../05-reference/08-session-format.md).

## Manage conversation context

The model receives the active branch, not every branch in the session file. Pi combines that history with the system prompt, discovered context files, available tools, and loaded skill descriptions. [How Pi Works](../01-get-started/03-how-pi-works.md#context) describes how those inputs are assembled.

The footer shows current context usage. When the active context approaches the model's limit, Pi normally compacts older history automatically. Compaction adds a summary and keeps recent messages. It does not delete the original session entries.

Run `/compact` to compact manually. You can add instructions when the summary should preserve a particular topic or decision. Configure automatic compaction and retained history through [Settings](../05-reference/04-settings.md#compaction).

Compaction can fail if the provider is unavailable or cannot accept the summarization request. Correct the provider problem and run `/compact` again. Disabling automatic compaction does not disable the manual command.

See [Compaction Reference](../05-reference/09-compaction.md) for thresholds, retained boundaries, branch-summary behavior, and extension hooks.

## Control session storage

By default, Pi stores sessions under `~/.pi/agent/sessions/`, grouped by working directory. Use `--session-dir`, `PI_CODING_AGENT_SESSION_DIR`, or the `sessionDir` setting to choose another location. The CLI option has highest precedence.

Use `--no-session` for an ephemeral run. An ephemeral session cannot be resumed after Pi exits.

Use `--session` when you already know the session path or ID. Use `--fork` to create a new session from an existing session before interactive mode starts.

## Export or share a session

Use `/export` to write the current session as HTML or JSONL. Use `/share` to upload it and get a viewer link. Pi uses a Radius artifact when Radius authentication is configured; otherwise, it uses a private GitHub gist.

Review exported or shared sessions first. They can contain prompts, model responses, tool arguments, command output, file contents, and extension messages.

## Report a bug

Run `/bug [description]` to prepare a private report for the Pi developers. You can include the session transcript, omit it, or ask the current model to summarize the problem. Review any transcript or generated summary because it can contain sensitive conversation data.

The report includes environment and provider configuration without credential values, plus recorded error diagnostics. Upload it through `radius.pi.dev` or export the same report as a zip to inspect and share yourself. Uploads do not require a login; Radius authentication attributes the report to your account so the developers can follow up. If an upload fails, Pi offers to export the zip.


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/04-security.md -->
<!-- ============================================================ -->

# Run Pi safely

Treat model-generated commands and code as untrusted. Pi can read, change, and execute files with the permissions of the account that started it, and it does not ask for approval before every tool call. Extensions, package installers, language servers, and other child processes run with those same permissions unless an operating-system or virtualization boundary restricts them.

Files, comments, instructions, command output, and model responses can steer the model through prompt injection. Project trust controls which project resources load at startup, but it does not make that content or the resulting actions safe.

Safety comes from limiting the files, credentials, processes, and network services Pi can access and affect if a generated action is wrong or hostile. Watching the transcript, using project trust, and reviewing changes do not create a security boundary.

## Choose how to run Pi

Different ways of running Pi place different limits on what generated commands can access:

| How Pi runs | What remains protected |
|---|---|
| Directly, with the permissions of its operating-system user | Anything that user cannot access. A dedicated user account can narrow those permissions, but Pi still shares the operating system and network with other users. |
| Entirely inside a container, virtual machine, or sandbox | Host files and processes that you do not expose to the environment. Credentials and network services remain accessible if you make them available inside it. This is usually the strongest practical option. |
| Outside the isolated environment, with only its built-in tools running inside | Host resources are protected from actions performed through those tools. Pi itself and other extensions remain outside the boundary, so this is a narrower form of isolation. |

The working folder controls resource discovery and the default location for tools, but it does not prevent commands from accessing other paths available to the Pi process.

Whichever option you choose, only provide the files and services required for the task. Keep credentials outside the environment where possible, or use narrowly scoped, short-lived credentials. Restrict network access when commands do not need it.

For setup instructions and the limitations of each isolation method, see [Run Pi in an isolated environment](../02-run-pi/05-containerization.md).

<a id="project-trust"></a>

## Understand project trust

Project trust controls whether Pi loads most settings and resources supplied by a working folder. It prevents a folder from silently loading executable extensions before you approve it.

Project trust is not a complete startup boundary. Pi reads the project `sessionDir` setting while selecting or creating a session, before it resolves project trust. Declining trust prevents the remaining project settings and protected resources from loading, but it cannot undo that initial session-directory lookup.

Project trust does not limit what tool calls can access or affect. After Pi starts, enabled tools still use the operating-system permissions of the Pi process. Instructions and other content in the folder can also influence the model.

### Resources protected by project trust

Pi requires a project-trust decision when it finds any of these resources from the current working directory:

- `.pi/settings.json`
- `.pi/mcp.json`
- `.pi/extensions`, `.pi/skills`, `.pi/prompts`, or `.pi/themes`
- `.pi/SYSTEM.md` or `.pi/APPEND_SYSTEM.md`
- project `.agents/skills` in the current directory or an ancestor directory

A bare `.pi` directory does not require project trust.

Granting project trust allows Pi to load:

- project settings
- project MCP servers from `.pi/mcp.json`
- extensions, skills, prompt templates, themes, and system-prompt files under `.pi`
- missing packages configured through project settings
- project-local and project-package extensions

Declining project trust skips those protected resources, except for the initial `sessionDir` lookup described above.

Context files such as `AGENTS.override.md`, `AGENTS.md`, and `CLAUDE.md` load regardless of project trust unless you disable context loading. Treat instructions in a folder as untrusted input even when you decline project trust.

### How Pi chooses a trust decision

A command-line `--approve` or `--no-approve` override applies first. When protected resources exist and there is no command-line override:

1. User-level and command-line extensions can handle the `project_trust` event. The first extension that returns yes or no owns the decision.
2. If no extension decides, Pi looks for a saved decision for the current directory or one of its parents. The closest decision applies.
3. If no saved decision applies, Pi follows the global `defaultProjectTrust` setting, whose default is `"ask"`.

Saved decisions use canonical directory paths and live in:

```text
~/.pi/agent/trust.json
```

Use `/trust` to save a decision for future Pi processes.

### Project trust without an interactive prompt

Print, JSON, and RPC modes cannot show the built-in trust prompt. If no command-line override, extension, or saved decision applies:

- `defaultProjectTrust: "always"` loads protected project resources.
- `defaultProjectTrust: "ask"` or `"never"` skips them.

Use `--approve` or `--no-approve` when an automated run needs an explicit one-time decision.

## Reduce impact and improve recovery

These practices do not replace isolation, but they reduce exposure or make recovery easier:

- Give Pi access only to files and services required for the task.
- Use snapshots, backups, or version control before substantial changes.
- Review extensions and packages before loading them. Extensions execute inside the Pi process.
- Prefer narrowly scoped, short-lived credentials.
- Review diffs and generated output before applying results to another system.
- Review sessions before exporting or sharing them. They can contain prompts, tool arguments, command output, file contents, and credentials exposed during the conversation.

## Report a security issue

Follow the repository [Security Policy](https://github.com/earendil-works/pi/blob/main/SECURITY.md). Do not open a public issue for a security-sensitive report.

Expected local-agent behavior, prompt injection from untrusted content, lack of a built-in sandbox, and behavior from user-installed extensions or skills are generally outside the security boundary unless the report demonstrates a privilege-boundary bypass or access that the local user did not already have.


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/05-containerization.md -->
<!-- ============================================================ -->

# Run Pi in an isolated environment

Use an isolated environment to limit the files, credentials, processes, and network services that generated commands can access or affect.

You can isolate the complete Pi process or keep Pi on the host and route selected tools into an isolated environment.

## Choose an isolation method

| Method | Where Pi runs | What is isolated | Credential handling | Best for |
|---|---|---|---|---|
| Plain Docker | Container | Pi, built-in tools, `!` commands, and extensions | Credentials passed into the container | A straightforward local container boundary |
| Docker Sandboxes | Managed sandbox | Pi, built-in tools, `!` commands, and extensions | Provider credentials remain on the host and are substituted by the proxy | Managed local isolation without exposing the real provider key |
| OpenShell | Local or remote sandbox | Pi, built-in tools, `!` commands, and extensions | Policy-controlled credentials and inference routing | Filesystem, process, network, and credential policies |
| Gondolin extension | Host | Built-in tools and `!` commands | Stored Pi credentials remain on the host, but commands inherit host environment variables | A local micro-VM for tool execution while retaining the host interface |

The method changes where extensions run. When the complete Pi process runs inside an isolated environment, its extensions run there too. When host Pi delegates built-in tools through Gondolin, other extension tools still run on the host unless they also delegate their work.

## Decide what Pi can access

An isolated process can still affect resources you expose to it:

- A read-write host mount lets Pi modify those host files.
- Mounting `~/.pi/agent` exposes your Pi credentials, settings, extensions, and sessions.
- Environment variables passed into a container are available to processes inside it.
- Network access may allow code or tool output to leave the environment.
- Tool-only isolation does not constrain the host Pi process or extension tools that do not use the isolated backend.

Expose only the working folder, credentials, and network destinations needed for the task. Use read-only mounts or copy files into and out of the environment when you do not want writes to affect the host.

## Run Pi in plain Docker

Plain Docker provides the simplest whole-process container boundary.

### Build the image

Create `Dockerfile.pi`:

```dockerfile
FROM node:24-bookworm-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash ca-certificates git ripgrep \
  && rm -rf /var/lib/apt/lists/*
RUN npm install -g --ignore-scripts @earendil-works/pi-coding-agent

WORKDIR /workspace
ENTRYPOINT ["pi"]
```

Build it from the directory containing the file:

```bash
docker build -t pi-sandbox -f Dockerfile.pi .
```

### Start Pi

From the working folder you want Pi to access, run:

```bash
docker run --rm -it \
  -e ANTHROPIC_API_KEY \
  -v "$PWD:/workspace" \
  -v pi-agent-home:/root/.pi/agent \
  pi-sandbox
```

Replace `ANTHROPIC_API_KEY` with the credential required by your provider. The named `pi-agent-home` volume keeps container-local settings, credentials, and sessions between runs.

Do not mount the host's `~/.pi/agent` unless the container should have access to your host Pi configuration and credentials.

### Verify the workspace

Inside Pi, run:

```text
!pwd
```

The command should report `/workspace`. Changes under `/workspace` write through to the mounted host folder. Remove the bind mount or use a read-only mount when that is not acceptable.

## Run Pi with Docker Sandboxes

[Docker Sandboxes](https://docs.docker.com/ai/sandboxes/) runs the complete Pi process inside a managed sandbox. Its proxy can keep the real provider credential on the host and substitute it when requests leave the sandbox.

Configure credentials before creating the sandbox. Do not run `/login` inside the sandbox because that writes a real credential into it.

### Use a Claude Pro or Max token

Generate the token with `claude setup-token` on a machine with Claude Code. If an `anthropic` secret is already configured, remove it first so the proxy does not add an API-key header alongside the bearer token:

```bash
sbx secret rm anthropic

sbx secret set-custom \
  --host api.anthropic.com \
  --env ANTHROPIC_OAUTH_TOKEN \
  --placeholder 'sk-ant-oat01-{rand}'
```

`sbx secret set-custom` reads the real token from standard input. The sandbox receives an OAuth-shaped placeholder, which the proxy replaces only for requests to the configured host.

For an Anthropic API key, use `sbx secret set anthropic` instead.

### Start Pi

Run this from the working folder you want mounted:

```bash
sbx run --kit "docker.io/sbx/pi-kit:latest" pi
```

For an existing sandbox, run Pi non-interactively with:

```bash
sbx exec <sandbox-name> -- pi -p "list the failing tests"
```

See the [Pi kit documentation](https://github.com/docker/sbx-kits-contrib/tree/main/pi) for other providers, troubleshooting, and image pinning.

## Run Pi with OpenShell

[NVIDIA OpenShell](https://docs.nvidia.com/openshell/about/overview) provides local or remote sandboxes with filesystem, process, network, credential, and inference policies.

### Select a gateway

Every sandbox requires an active gateway:

```bash
openshell gateway add <gateway-url> --name <name>
openshell gateway select <name>
```

### Create the sandbox

```bash
openshell sandbox create --name pi-sandbox --from pi -- pi
```

Pi, its built-in tools, `!` commands, and extension tools run inside the OpenShell boundary.

### Transfer files to a remote sandbox

A remote gateway does not bind-mount your host working folder. Clone the repository inside the sandbox or transfer files explicitly:

```bash
openshell sandbox upload pi-sandbox ./working-folder /workspace
openshell sandbox download pi-sandbox /workspace/working-folder ./working-folder-out
```

OpenShell inference routing can keep raw model credentials outside the sandbox. When configured, point Pi at the corresponding OpenAI-compatible or Anthropic-compatible endpoint exposed by the gateway.

## Route tools through Gondolin

[Gondolin](https://github.com/earendil-works/gondolin) is a local Linux micro-VM. Its example extension keeps the Pi process and file-based provider credentials on the host while routing the built-in tools and user `!` commands into the VM.

Commands inside the VM inherit the host process environment. Provider keys supplied through environment variables can therefore be visible inside the VM. Do not use this pattern as a credential boundary unless you remove sensitive variables or change the extension's environment handling.

Gondolin requires Node.js 23.6 or newer and QEMU installed through your operating-system package manager.

### Install the extension

From a Pi source checkout:

```bash
mkdir -p ~/.pi/agent/extensions
cp -R packages/coding-agent/examples/extensions/gondolin ~/.pi/agent/extensions/gondolin
cd ~/.pi/agent/extensions/gondolin
npm install --ignore-scripts
```

### Start Pi

Run Pi from the working folder you want mounted:

```bash
cd /path/to/working-folder
pi -e ~/.pi/agent/extensions/gondolin
```

The extension mounts the host working folder at `/workspace` in the VM and overrides `read`, `write`, `edit`, `bash`, `grep`, `find`, and `ls`. File changes under `/workspace` write through to the host.

Other extension tools still run on the host unless they explicitly delegate their operations. Review the [Gondolin example](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/gondolin/) before adding tools that could bypass the VM boundary.


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/06-llama-cpp.md -->
<!-- ============================================================ -->

# Local Models with llama.cpp

Pi supports the [llama.cpp](https://github.com/ggml-org/llama.cpp) router server. The router discovers multiple GGUF models and loads or unloads them on demand.

Use a current llama.cpp build with router support. Follow the [build instructions](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md) or install a [prebuilt release](https://github.com/ggml-org/llama.cpp/releases) for your platform.

## Start the router

Start `llama-server` without `--model` or `-m`. Passing a model starts single-model mode instead of router mode.

```bash
llama-server \
  --models-dir ~/models \
  --no-models-autoload \
  --jinja \
  --host 127.0.0.1 \
  --port 8080 \
  -ngl 999 \
  -c 32768
```

Important options:

- `--models-dir ~/models` discovers local GGUF files.
- `--no-models-autoload` keeps loading explicit through `/llama`.
- `--jinja` enables compatible chat templates and tool calling.
- `-ngl 999` offloads as many layers as possible to the GPU.
- `-c 32768` sets the context window for each loaded model. Omit it to use the model's native context, which may require substantially more memory.

A single-file model can sit directly in the model directory. Put multimodal and multi-shard models in separate subdirectories:

```text
~/models/
├── llama-3.2-1b-Q4_K_M.gguf
├── gemma-3-4b-it-Q4_K_M/
│   ├── gemma-3-4b-it-Q4_K_M.gguf
│   └── mmproj-F16.gguf
└── large-model-Q4_K_M/
    ├── large-model-Q4_K_M-00001-of-00003.gguf
    ├── large-model-Q4_K_M-00002-of-00003.gguf
    └── large-model-Q4_K_M-00003-of-00003.gguf
```

Restart the router after manually adding files. For per-model context sizes and other options, use [llama.cpp model presets](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md#model-presets).

## Configure Pi

Start Pi and configure the provider:

```text
/login llama.cpp
```

Enter the router URL and optional API key. The default URL is `http://127.0.0.1:8080`.

If you start the router with `--no-models-autoload`, `/login llama.cpp` only stores the connection. Run `/llama` to load a model, then `/model` to select the loaded model for the current session.

Environment variables can configure the same values without `/login`:

```bash
export LLAMA_BASE_URL=http://127.0.0.1:8080
export LLAMA_API_KEY=optional-secret
pi
```

If the server uses an API key, start `llama-server` with the matching `--api-key` value. Keep `--host 127.0.0.1` for local-only access.

## Manage models

Run:

```text
/llama
```

- Select an unloaded model to load it.
- Select a loaded model to unload it.
- Select **Download model…**, search Hugging Face, then choose a repository and quantization. Exact `owner/repository[:quant]` values also work.
- Press Escape during a load or download to confirm cancellation.

Hugging Face search uses `HF_TOKEN` when set, then checks `$HF_TOKEN_PATH`, `$HF_HOME/token`, `$XDG_CACHE_HOME/huggingface/token`, and `~/.cache/huggingface/token`. Search also works without authentication, subject to lower rate limits. Pi warns before downloading gated repositories and links to their access page. The llama.cpp server performs the download, so its process must also have `HF_TOKEN` when the selected repository requires access.

If other models are loaded, Pi asks whether to unload them first or keep them loaded. Pi does not silently unload models and never deletes model files. The router may be shared with other clients, so `/llama` always displays the router's current state.

Loaded and sleeping models appear in `/model`. Sleeping models wake automatically when selected. With router autoload enabled, unloaded preset models also appear and load when selected. With `--no-models-autoload`, load a model through `/llama` before selecting it.

If the router disconnects, `/llama` shows **Retry** and **Close**. Retry reconnects and refreshes model state without replaying the interrupted operation.

## Classification

Every model listed for chat is also listed as a classifier model with the same ID and the `llama-cpp-classify` API. Classifier models answer typed `choice`, `bool`, and `score` questions about JSON state, like TypeSafe's Jev models. The model reaches them from [`codemode`](../05-reference/01-cli.md#enable-codemode) scripts, and extensions through `ctx.modelRegistry.classify()`; see [Classifier models](../02-run-pi/02-models.md#use-classifier-models).

The model does not generate an answer. Each question becomes one chat prompt: the state, every question of the request, the state again, and then the question with its answers under single-token labels. Labels are letters for a choice (up to 62 options), `Yes`/`No` for a bool, and digits for a score (up to 10 levels). The second copy of the state is read with the questions in view, which improved accuracy on JevBench with small models. Pi reads the probabilities of the labels as the next token and normalizes them. A choice returns every option's probability and a confidence of `(n * peak - 1) / (n - 1)`; a score returns the expected level.

- Raw label probabilities are usually overconfident. The per-request `temperature` option divides the label logits before normalizing; values above 1 soften the distribution. It changes no answer.
- Questions run one after another. Everything before the final question is the same for all questions of a request, so the server's prompt cache evaluates it once. The state appears twice, so it needs twice its size in context.
- Small models may follow instructions written inside the state. The prompt tells the model to judge the state as data, but that is not a guarantee.
- Hybrid models such as Qwen3.5 cannot rewind a partially cached prompt without context checkpoints. If each question reprocesses the whole state, start the router with `--ctx-checkpoints 32 --checkpoint-min-step 0`.

## Troubleshooting

Check that the router is reachable:

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/models
```

- **No models in `/llama`:** Check `--models-dir`, the directory layout, and restart the router.
- **Model missing from `/model` with `--no-models-autoload`:** Load it with `/llama` first.
- **Load fails or uses too much memory:** Lower `-c` or unload another model.
- **Server is not in router mode:** Start it without `--model`, `-m`, or `-hf`.

To remove the `llama.cpp` provider and `/llama`, disable `llama.cpp` under Built-in in `pi config`, or set `"extensions": ["-builtin:llama.cpp"]` in [settings](../05-reference/04-settings.md#resources).


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/07-terminal-setup.md -->
<!-- ============================================================ -->

# Configure your terminal

Most modern terminals work with Pi without additional setup. Use this page when modified keys, scrolling, links, images, colors, or input-method editor (IME) positioning do not behave as expected.

Pi uses extended-key protocols so terminals can distinguish combinations such as `Shift+Enter` and `Alt+Enter` from plain `Enter`. Terminal proxies, multiplexers, and built-in IDE terminals can change or discard that information.

## Troubleshooting

| Symptom | Start here |
|---|---|
| `Shift+Enter` submits instead of inserting a line | Your terminal's section below; for tmux, see [Run Pi in tmux](../02-run-pi/09-tmux.md) |
| `Alt+Enter` does not queue a follow-up | [WezTerm](#wezterm), [Alacritty](#alacritty), or [Windows Terminal](#windows-terminal) |
| Fullscreen scrolling is unusually slow | [iTerm2](#iterm2) |
| Links work but show no hover preview | [Ghostty](#ghostty) |
| Inline images or colors are not detected | [Override detected capabilities](#override-detected-capabilities) |
| An IME candidate window appears in the wrong place | [WezTerm](#wezterm) or [IntelliJ IDEA](#intellij-idea-integrated-terminal) |
| Modified keys fail only inside tmux | [Run Pi in tmux](../02-run-pi/09-tmux.md) |

Use `/hotkeys` to inspect Pi's active shortcuts. See [Keybindings](../05-reference/06-keybindings.md) to change them.

## Kitty

Kitty supports the required keyboard protocol without additional configuration.

## iTerm2

Regular terminal mode works without additional configuration.

### Fix slow fullscreen scrolling

In fullscreen mode, Pi owns the viewport, so iTerm2 sends mouse-wheel reports instead of scrolling native terminal history. Fast trackpad gestures can then move only about one line at a time.

To change this behavior:

1. Open **iTerm2 > Settings > Advanced**.
2. Search for **Trackpad scrolls fast?**.
3. Set it to **No**.

This is an iTerm2-wide setting and can also change native trackpad scrolling. The underlying behavior is tracked in [iTerm2 issue 9619](https://gitlab.com/gnachman/iterm2/-/work_items/9619).

## Apple Terminal

Pi enables enhanced key reporting when available. If Terminal.app still sends plain Return for `Shift+Enter`, Pi uses a local macOS modifier fallback and treats it as `Shift+Enter`.

The fallback works only when Pi runs on the same Mac as Terminal.app. It cannot inspect the local modifier state when Pi runs on another machine over SSH.

## Ghostty

Add this mapping to Ghostty's configuration if `Alt+Backspace` does not work:

```text
keybind = alt+backspace=text:\x1b\x7f
```

The configuration file is `~/Library/Application Support/com.mitchellh.ghostty/config` on macOS and `~/.config/ghostty/config` on Linux.

Older Claude Code configurations may contain:

```text
keybind = shift+enter=text:\n
```

This sends a raw linefeed, which Pi cannot distinguish from `Ctrl+J`. Remove the mapping if an older Claude Code installation is the only reason you added it. Pi already binds `Ctrl+J` as a newline alternative, so the mapping may appear to work while still preventing Pi and tmux from receiving a real `Shift+Enter` event.

### Open links in fullscreen mode

Links remain clickable in fullscreen mode, but Ghostty does not show its normal hover underline or URL preview while Pi captures mouse input. Hold `Shift+Command` on macOS or `Shift+Ctrl` on Linux to use Ghostty's native link handling.

## WezTerm

WezTerm normally reports `Shift+Enter` through xterm extended keys. To enable the Kitty keyboard protocol explicitly, create `~/.wezterm.lua`:

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()
config.enable_kitty_keyboard = true
return config
```

### Forward Alt+Enter on macOS

WezTerm binds `Option+Enter` to fullscreen by default on macOS. To use it for Pi's follow-up queue, add this entry to your `config.keys` table:

```lua
{
  key = 'Enter',
  mods = 'ALT',
  action = wezterm.action.SendString('\x1b[13;3u'),
}
```

A complete minimal configuration is:

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()
config.keys = {
  {
    key = 'Enter',
    mods = 'ALT',
    action = wezterm.action.SendString('\x1b[13;3u'),
  },
}
return config
```

### Position an IME candidate window in WSL

If CJK IME candidates do not follow Pi's text cursor in WSL, show the hardware cursor:

```bash
export PI_HARDWARE_CURSOR=1
pi
```

You can instead set `showHardwareCursor` to `true` in Pi settings.

## Alacritty

Alacritty normally reports `Shift+Enter`. On macOS, `Option+Enter` can arrive as plain `Enter`. Add this to `~/.config/alacritty/alacritty.toml` to forward it to Pi:

```toml
[[keyboard.bindings]]
key = "Enter"
mods = "Alt"
chars = "\u001b[13;3u"
```

Restart Alacritty after changing the file.

## VS Code integrated terminal

VS Code 1.109.5 and newer enable the Kitty keyboard protocol in the integrated terminal by default.

For an older version, add a `Shift+Enter` terminal binding to `keybindings.json`:

```json
{
  "key": "shift+enter",
  "command": "workbench.action.terminal.sendSequence",
  "args": { "text": "\u001b[13;2u" },
  "when": "terminalFocus"
}
```

The user `keybindings.json` file is normally located at:

- macOS: `~/Library/Application Support/Code/User/keybindings.json`
- Linux: `~/.config/Code/User/keybindings.json`
- Windows: `%APPDATA%\\Code\\User\\keybindings.json`

## Zed integrated terminal

Add these bindings to Zed's `keymap.json`:

```json
{
  "context": "Terminal",
  "bindings": {
    "shift-enter": ["terminal::SendText", "\u001b[13;2u"],
    "ctrl--": ["terminal::SendText", "\u001b[45;5u"],
    "ctrl-alt-]": ["terminal::SendText", "\u001b[93;7u"]
  }
}
```

## Windows Terminal

Windows Terminal uses Pi's Windows and WSL shortcut defaults. See [Keybindings](../05-reference/06-keybindings.md) for the complete list.

### Forward Shift+Enter

Open Windows Terminal's `settings.json` with `Ctrl+Shift+,` or **Settings > Open JSON file**. Add this object to its `actions` array:

```json
{
  "command": { "action": "sendInput", "input": "\u001b[13;2u" },
  "keys": "shift+enter"
}
```

Fully close and reopen Windows Terminal, then verify that `Shift+Enter` inserts a new line in Pi.

### Use Alt+Enter for follow-ups

Windows Terminal binds `Alt+Enter` to fullscreen by default. Pi therefore uses `Ctrl+Q` for follow-ups on Windows and WSL.

To use `Alt+Enter` instead, configure Windows Terminal to forward the key and bind `app.message.followUp` to `alt+enter` in Pi's `keybindings.json`. See [Keybindings](../05-reference/06-keybindings.md#assign-keybindings).

## xfce4-terminal and Terminator

These terminals cannot reliably distinguish modified Enter keys from plain `Enter`. Custom bindings such as `Ctrl+Enter` or `Shift+Enter` therefore may not work.

Use a terminal with modern extended-key support when you need those shortcuts, such as Kitty, Ghostty, WezTerm, iTerm2, Windows Terminal, or a compatible Alacritty build.

## IntelliJ IDEA integrated terminal

IntelliJ IDEA's built-in terminal cannot reliably distinguish `Shift+Enter` from plain `Enter`. Use `Ctrl+J` for a newline or run Pi in a terminal with modern extended-key support.

If an IME candidate window does not follow the text cursor, show the hardware cursor:

```bash
export PI_HARDWARE_CURSOR=1
pi
```

## Override detected capabilities

Pi automatically detects OSC 8 hyperlinks, inline image protocols, and truecolor support. A terminal proxy or multiplexer can make that detection inaccurate.

| Capability | Environment variable | Setting |
|---|---|---|
| Hyperlinks | `PI_HYPERLINKS=1\|0\|auto` | `terminal.hyperlinks: true\|false\|"auto"` |
| Inline images | `PI_IMAGE_PROTOCOL=kitty\|iterm2\|none\|auto` | `terminal.images: "kitty"\|"iterm2"\|false\|"auto"` |
| Truecolor | `PI_TRUE_COLOR=1\|0\|auto` | `terminal.trueColor: true\|false\|"auto"` |

Settings take precedence over environment variables. An unset value or `auto` preserves automatic detection.

Only force a capability supported by the complete terminal path. Unsupported escape sequences can corrupt rendering. See [Environment Variables](../05-reference/05-environment-variables.md#pi-process-configuration) and [Settings](../05-reference/04-settings.md) for the canonical value definitions.


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/08-shell-aliases.md -->
<!-- ============================================================ -->

# Configure shell commands

Pi starts a separate non-interactive shell process for each Bash command. Non-interactive Bash does not expand aliases by default and usually does not load the same startup files as an interactive terminal.

Use `shellPath` to choose the Bash executable and `shellCommandPrefix` to run setup before each command.

## Understand which shell Pi uses

| Command source | Shell |
|---|---|
| Model calls the built-in `bash` tool | Pi's resolved Bash executable |
| You enter `!command` or `!!command` | The same resolved Bash executable |
| Model calls the optional `powershell` tool | PowerShell 7 (`pwsh.exe`) or Windows PowerShell |
| An extension provides or replaces a shell tool | The operations implemented by that extension |

Pi normally invokes Bash with `bash -c`. On Unix systems, it uses `/bin/bash`, then `bash` on `PATH`, and finally `sh` when Bash is unavailable. Native Windows first checks the configured path, then Git Bash, then `bash.exe` on `PATH`.

## Choose a Bash executable

Set `shellPath` in `~/.pi/agent/settings.json` when Pi should use a specific executable:

```json
{
  "shellPath": "~/.local/bin/bash"
}
```

On Windows, use forward slashes or escape backslashes:

```json
{
  "shellPath": "C:\\cygwin64\\bin\\bash.exe"
}
```

Run `/reload` after changing the setting. See [Run Pi on Windows](../02-run-pi/10-windows.md) for the native Windows defaults.

## Run setup before every Bash command

Set `shellCommandPrefix` to prepend shell setup to both the built-in `bash` tool and user-entered `!` or `!!` commands:

```json
{
  "shellCommandPrefix": "export CI=1"
}
```

Pi joins the prefix and requested command with a newline. The prefix runs again for every command, so keep it fast and free of interactive prompts.

## Enable Bash aliases

Store aliases needed by Pi in a Bash-compatible file instead of parsing an entire interactive shell configuration.

Create `~/.bash_aliases`:

```bash
alias ll='ls -la'
alias gs='git status --short'
```

Then configure Pi to enable alias expansion and load the file:

```json
{
  "shellCommandPrefix": "shopt -s expand_aliases\nsource ~/.bash_aliases"
}
```

Run `/reload`, then verify the alias through Pi:

```text
!ll
```

The command should produce the same listing as `ls -la`.

Aliases must use Bash-compatible syntax. Do not source an arbitrary `.zshrc` into Bash because zsh options, functions, and plugins may not parse or behave correctly there.

## Troubleshooting

### The prefix works for `!` but not for an extension tool

`shellCommandPrefix` configures Pi's built-in Bash execution. An extension that replaces the `bash` tool or provides its own shell operations controls its own setup. Check that extension's documentation.

### `shopt` is not found

Pi has fallen back to `sh` or `shellPath` points to a non-Bash shell. Install Bash or set `shellPath` to a Bash executable before using Bash-specific setup such as `shopt`.

### A setup command waits for input

Remove interactive commands from `shellCommandPrefix`. The prefix runs in a non-interactive process before every Bash command.

For the complete setting definitions, see [Shell settings](../05-reference/04-settings.md#shell).


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/09-tmux.md -->
<!-- ============================================================ -->

# Run Pi in tmux

Pi works inside tmux, but tmux can report `Shift+Enter`, `Ctrl+Enter`, and plain `Enter` as the same key. Enable extended keys so Pi can distinguish them.

## Check your tmux version

```bash
tmux -V
```

For tmux 3.5 or newer, use the recommended CSI-u configuration below. For tmux 3.2 through 3.4, use the older-version configuration.

## Enable extended keys in tmux 3.5 or newer

Add these lines to `~/.tmux.conf`:

```tmux
set -g extended-keys on
set -g extended-keys-format csi-u
```

Pi requests extended-key reporting when the terminal does not provide the Kitty keyboard protocol directly. CSI-u is the most reliable format for forwarding modified keys through tmux.

## Restart tmux

The configuration applies to the tmux server. To guarantee that it is active, close your tmux sessions and start a new server.

If you choose to stop the server from the command line, save your work first. This command terminates every session managed by that server:

```bash
tmux kill-server
tmux
```

## Verify modified keys

Start Pi inside the new tmux session and check that:

1. `Shift+Enter` inserts a new line in the editor.
2. `Enter` submits the prompt.
3. `Alt+Enter` queues a follow-up on macOS and Linux. Windows and WSL use `Ctrl+Q` by default.

If these keys still behave like plain `Enter`, verify that the terminal outside tmux can report modified keys. See [Configure your terminal](../02-run-pi/07-terminal-setup.md).

## Use tmux 3.2 through 3.4

These versions support extended keys but not `extended-keys-format csi-u`. Add only:

```tmux
set -g extended-keys on
```

Pi supports the xterm `modifyOtherKeys` format used by these versions. Restart tmux and repeat the verification steps.

For older versions, upgrade tmux or use Pi outside tmux rather than relying on modified Enter shortcuts.


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/10-windows.md -->
<!-- ============================================================ -->

# Run Pi on Windows

Run Pi either as a native Windows process or inside Windows Subsystem for Linux (WSL). Native Windows uses Git Bash by default for Bash commands and can optionally expose PowerShell to the model. Pi inside WSL uses the Linux environment and its Bash installation.

Follow the main [Quickstart](../01-get-started/02-quickstart.md) to install and authenticate Pi. Use this page to choose and configure its command environment.

## Choose native Windows or WSL

| Environment | Command environment | Use it when |
|---|---|---|
| Native Windows with Git Bash | Git Bash for the built-in `bash` tool and `!` commands | Your files and development tools primarily live on Windows |
| Native Windows with the `powershell` tool | PowerShell for model tool calls; Bash remains available for `!` commands | The task depends on PowerShell modules or Windows-native commands |
| WSL | Linux Bash and tools inside the selected WSL distribution | Your files and toolchain already live in Linux or WSL |

## Use Git Bash on native Windows

For most native Windows users, installing [Git for Windows](https://git-scm.com/download/win) is sufficient.

Pi resolves Bash in this order:

1. `shellPath` from `~/.pi/agent/settings.json`
2. Git Bash under `Program Files` or `Program Files (x86)`
3. `bash.exe` on `PATH`, including Cygwin, MSYS2, or legacy WSL Bash

Start Pi and enter this command to verify the shell:

```text
!printf 'Bash is working\n'
```

If Pi cannot find Bash, it reports the locations it checked. Install Git for Windows, put another Bash executable on `PATH`, or configure `shellPath`.

## Let the model use PowerShell

The optional `powershell` tool runs commands through `pwsh.exe` when available, then falls back to Windows PowerShell. It starts PowerShell with `-NoProfile -NonInteractive -ExecutionPolicy Bypass`. Administrator-enforced execution policies can still take precedence.

To replace the model-facing `bash` tool with `powershell`, add this to `~/.pi/agent/settings.json`:

```json
{
  "defaultTools": ["read", "powershell", "edit", "write"]
}
```

`["-bash", "+powershell"]` does the same while keeping any other default tools you configured.

Restart Pi, then ask it to run a harmless PowerShell command. The `!` and `!!` editor commands continue to use Bash. The `powershell` tool is available only when Pi runs as a native Windows process.

See [Settings](../05-reference/04-settings.md#tools) for other tool combinations.

## Use a custom Bash executable

Set `shellPath` when Bash is installed somewhere Pi does not discover automatically:

```json
{
  "shellPath": "C:\\cygwin64\\bin\\bash.exe"
}
```

JSON uses backslashes for escape sequences. When you write a Windows path with backslashes, write each backslash twice, as shown above.

See [Configure shell commands](../02-run-pi/08-shell-aliases.md) for command prefixes, aliases, and the complete shell-resolution behavior.

## Configure Windows Terminal

Windows Terminal reserves or rewrites some modified keys. See [Windows Terminal](../02-run-pi/07-terminal-setup.md#windows-terminal) to configure `Shift+Enter` and `Alt+Enter`, and [Keybindings](../05-reference/06-keybindings.md) for Pi's Windows and WSL shortcut defaults.


<!-- ============================================================ -->
<!-- SOURCE: 02-run-pi/11-termux.md -->
<!-- ============================================================ -->

# Run Pi on Android with Termux

Pi runs on Android through [Termux](https://termux.dev/), a terminal emulator and Linux environment. Text input, file tools, and shell commands are supported. Pi can copy and paste text through the Android clipboard with Termux:API. Clipboard image paste is not supported.

## Before you begin

Install Termux from [GitHub or F-Droid](https://github.com/termux/termux-app#installation). Do not use the deprecated Google Play build.

[Termux:API](https://github.com/termux/termux-api#installation) is optional. Install it only when you want Pi to copy or paste Android clipboard text, or when shell commands need Android device APIs.

## Install Pi

1. Update Termux packages:

   ```bash
   pkg update && pkg upgrade
   ```

2. Install Node.js and Git:

   ```bash
   pkg install nodejs git
   ```

3. Install Pi:

   ```bash
   npm install -g --ignore-scripts @earendil-works/pi-coding-agent
   ```

4. Verify the installation:

   ```bash
   pi --version
   ```

5. Open the folder you want to work in and start Pi:

   ```bash
   cd /path/to/working-folder
   pi
   ```

Continue with the main [Quickstart](../01-get-started/02-quickstart.md#3-choose-a-model) to connect a model and run your first task.

## Access Android shared storage

Termux cannot access shared Android storage until you grant permission. Run this once:

```bash
termux-setup-storage
```

After approval, Android shared storage is available under `/storage/emulated/0` and through the links Termux creates under `~/storage/`.

Only grant this permission when Pi should be able to access those files. Commands and tools running in Termux use the same storage permissions as the Termux process.

## Use clipboard commands

Pi uses `termux-clipboard-set` to copy text and `termux-clipboard-get` for its clipboard-paste shortcut. Shell commands can use both commands directly. Install the Termux:API app and its command-line package:

```bash
pkg install termux-api
```

Verify the integration:

```bash
printf 'Pi clipboard test' | termux-clipboard-set
termux-clipboard-get
```

The second command should print `Pi clipboard test`.

The Termux clipboard API supports text only. Pi's clipboard-paste shortcut inserts that text into the editor but cannot attach clipboard images.

## Add Termux-specific instructions

Pi detects that it is running in Termux, but it cannot infer how you want it to interact with Android. Add only the environment details relevant to your work to `~/.pi/agent/AGENTS.md`:

````markdown
# Termux environment

- Pi runs in Termux on Android.
- Shared Android storage is under `/storage/emulated/0`.
- Open URLs with `termux-open-url "https://example.com"`.
- Open files with `termux-open <path>`.
- Do not access shared storage unless the task requires it.
````

Run `/reload` after changing the file during an active session.

## Troubleshooting

### Clipboard integration fails

Confirm that you installed both components:

1. The Termux:API Android app from the same source as Termux
2. The `termux-api` command-line package

Then run the clipboard verification commands above outside Pi. If they fail there, fix the Termux:API installation before retrying Pi's copy command.

### Shared storage reports permission denied

Run `termux-setup-storage`, approve the Android permission request, and retry the path under `~/storage/` or `/storage/emulated/0`.

### Pi is not found after installation

Open a new Termux shell and run:

```bash
npm prefix -g
command -v pi
```

Confirm that the global npm binary directory is on `PATH`, then reinstall Pi if the package is missing.


<!-- ============================================================ -->
<!-- SOURCE: 03-customize-pi/01-configuration.md -->
<!-- ============================================================ -->

# Configuration

Pi supports user-level and project configuration. User-level configuration lives in the agent directory, which defaults to `~/.pi/agent`. Project configuration lives in `.pi` under the working directory and loads after [project trust](../02-run-pi/04-security.md#understand-project-trust) is granted. The only exception is `sessionDir`, which Pi reads before resolving trust so it can locate sessions.

In interactive mode, use `/settings` to change common preferences. For other options, ask Pi to update the configuration or edit the relevant files directly. Run `/reload` after manually changing settings, keybindings, instructions, or resources.

## Agent directory

The agent directory is shown as `<agent-dir>` below. Set its location with the `PI_CODING_AGENT_DIR` environment variable or the SDK's [`agentDir`](../04-build-on-pi/06-sdk.md) option.

| Path | Responsibility |
|---|---|
| `<agent-dir>/settings.json` | User-level [settings](../05-reference/04-settings.md), including preferences, defaults, resource paths, and Pi package declarations. |
| `<agent-dir>/keybindings.json` | Custom terminal UI and application [keybindings](../05-reference/06-keybindings.md). |
| `<agent-dir>/mcp.json` | [MCP servers](../03-customize-pi/06-mcp.md) available in every project. |
| `<agent-dir>/models.json` | [Compatible endpoints, models, and model overrides](../02-run-pi/02-models.md#configure-a-compatible-endpoint). |
| `<agent-dir>/auth.json` | Saved API keys and OAuth credentials. |
| `<agent-dir>/AGENTS.override.md`, `AGENTS.md`, `AGENTS.MD`, `CLAUDE.md`, or `CLAUDE.MD` | User instructions applied across working directories. |
| `<agent-dir>/SYSTEM.md` | Replaces Pi’s default system prompt. |
| `<agent-dir>/APPEND_SYSTEM.md` | Adds instructions to Pi’s system prompt. |
| `<agent-dir>/extensions/` | User [extensions](../04-build-on-pi/01-extensions.md). |
| `<agent-dir>/skills/` | User [skills](../03-customize-pi/03-skills.md) and supporting files. |
| `<agent-dir>/prompts/` | User [prompt templates](../03-customize-pi/02-prompt-templates.md) exposed as slash commands. |
| `<agent-dir>/themes/` | User [theme](../03-customize-pi/04-themes.md) files. |

## Project `.pi` directory

| Path | Responsibility |
|---|---|
| `.pi/settings.json` | Project-level [settings](../05-reference/04-settings.md), resource paths, and Pi package declarations. |
| `.pi/mcp.json` | Project [MCP servers](../03-customize-pi/06-mcp.md). |
| `.pi/SYSTEM.md` | Replaces the system prompt for the project. |
| `.pi/APPEND_SYSTEM.md` | Adds project-specific instructions to the system prompt. |
| `.pi/extensions/` | Project extensions. |
| `.pi/skills/` | Project skills and supporting files. |
| `.pi/prompts/` | Project prompt templates exposed as slash commands. |
| `.pi/themes/` | Project theme files. |

For `SYSTEM.md` and `APPEND_SYSTEM.md`, the trusted project file takes precedence over the corresponding agent-directory file. Files with the same name are not combined.

## Context files

Context files are separate from project `.pi` configuration. Pi loads them from the agent directory, the working directory, and its parent directories. A context file applies whenever Pi runs in its directory or anywhere below it.

An `AGENTS.override.md` replaces `AGENTS.md` or `CLAUDE.md` only in the same directory. It does not suppress context files from the agent directory or other directories.

Context-file discovery does not require project trust.


<!-- ============================================================ -->
<!-- SOURCE: 03-customize-pi/02-prompt-templates.md -->
<!-- ============================================================ -->

# Prompt Templates

Prompt templates turn Markdown files into reusable `/` commands. Use one when you want to reuse the same prompt without adding executable behavior or a larger set of supporting instructions.

A template can accept arguments and appear in command completion. Pi can load templates from personal configuration, project configuration, an explicit path, or a Pi package. Project configuration loads only after project trust is granted.

## Create a template

Create `~/.pi/agent/prompts/review.md`:

```markdown
---
description: Review staged git changes
argument-hint: "[focus]"
---
Review the staged changes. Focus on ${1:-correctness, security, and error handling}.
```

The filename becomes the command name, so this template is available as `/review`. The `description` appears in command completion. If it is omitted, Pi uses the first non-empty line.

`argument-hint` is optional. Use `<angle brackets>` for required arguments and `[square brackets]` for optional arguments.

Run `/reload` after adding or changing a template in an active session.

<a id="invoke-a-template"></a>

## Use a template

Type the template command in the editor:

```text
/review
/review concurrency
```

Pi expands the template before the resulting text enters the agent. Extensions receive the raw input first through the `input` event unless an extension command with the same name handles it.

Templates support these substitutions:

| Syntax | Result |
|---|---|
| `$1`, `$2`, … | One positional argument |
| `$@` or `$ARGUMENTS` | All arguments joined with spaces |
| `${1:-default}` | First argument, or a default value |
| `${@:-default}` | All arguments, or a default value |
| `${@:N}` | Arguments starting at position `N` |
| `${@:N:L}` | `L` arguments starting at position `N` |

Arguments follow shell-like quoting, so `/review "API compatibility"` supplies one argument containing a space.

<a id="choose-where-it-loads"></a>

## Add it to Pi

Place the template in your user or project prompt directory. Conventional prompt directories load direct `.md` children only.

Settings and packages can select nested Markdown files; a package manifest can narrow discovery with explicit paths and globs. See [Settings](../05-reference/04-settings.md#resources) and [Pi Packages](../03-customize-pi/05-packages.md) for these options.

Project templates become commands in the editor after trust is granted. Review their content before trusting an unfamiliar project. See [Security](../02-run-pi/04-security.md#understand-project-trust).


<!-- ============================================================ -->
<!-- SOURCE: 03-customize-pi/03-skills.md -->
<!-- ============================================================ -->

# Skills

Skills give Pi specialized instructions and supporting files for a particular kind of work. Pi advertises each available skill by name and description, then loads its full instructions only when the task calls for them.

Use a skill when a workflow needs more context than a prompt template but does not need a new executable integration point. Skills can bundle scripts, references, and assets alongside their instructions.

Pi implements the [Agent Skills specification](https://agentskills.io/specification). Most invalid fields produce warnings rather than stopping startup.

## Create a skill

A skill is a directory containing `SKILL.md`:

```text
pdf-tools/
├── SKILL.md
├── scripts/
│   └── extract.sh
├── references/
│   └── formats.md
└── assets/
    └── template.json
```

Start `SKILL.md` with frontmatter followed by direct instructions:

```markdown
---
name: pdf-tools
description: Extract text and tables from PDF files. Use when reading, converting, or inspecting PDFs.
---

# PDF tools

Read `references/formats.md` before converting a document. Run scripts relative to this skill directory.
```

The description determines when the model considers loading the skill. State both what the skill does and when it applies. Avoid descriptions such as “Helps with PDFs,” which do not provide enough routing information.

Use relative paths from the skill directory when referring to bundled files. Pi tells the model where the skill lives so it can resolve those paths.

## Understand how skills load

At startup, Pi scans configured skill locations and adds each skill’s name, description, and path to the system prompt. It does not add the full instructions.

When a task matches, the model reads `SKILL.md` and follows its instructions. This keeps detailed guidance out of context until it is needed. A model might fail to load a relevant skill, so use `/skill:name` when you need to force it.

Arguments after `/skill:name` are appended to the loaded instructions as a user request:

```text
/skill:pdf-tools extract report.pdf
```

Set `disable-model-invocation: true` in frontmatter when a skill should be available only through its explicit command. The `enableSkillCommands` [setting](../05-reference/04-settings.md) controls whether skill commands appear in interactive command discovery; manually entered `/skill:name` commands still work.

<a id="choose-where-it-loads"></a>

## Add it to Pi

Place the skill in your user or project skills directory. Directories containing `SKILL.md` are discovered recursively.

Pi also supports the Agent Skills locations `~/.agents/skills/` and `.agents/skills/`. Project `.agents/skills/` directories are discovered from the working directory through its ancestors, stopping at the repository root when one exists.

Pi accepts some standalone Markdown skills, but a directory containing `SKILL.md` is the portable form and should be preferred. See [Settings](../05-reference/04-settings.md#resources) and [Pi Packages](../03-customize-pi/05-packages.md) for additional locations.

Project skills can instruct the model to run scripts or modify files. Review unfamiliar skills and their supporting files before granting project trust.

## Write portable frontmatter

The Agent Skills specification defines these fields:

| Field | Purpose |
|---|---|
| `name` | Command and display name |
| `description` | Routing description shown to the model |
| `license` | License name or bundled license file |
| `compatibility` | Environment requirements |
| `metadata` | Additional key-value metadata |
| `allowed-tools` | Experimental pre-approved tool list |
| `disable-model-invocation` | Hide the skill from automatic model selection |

Names use lowercase letters, numbers, and hyphens, with no leading, trailing, or consecutive hyphens. They can contain at most 64 characters; descriptions can contain at most 1024.

Pi neither requires nor warns when the declared name differs from the parent directory. Other Agent Skills implementations may enforce that requirement, so matching names remain the portable choice.

Malformed `SKILL.md` files and declared skills without descriptions are not loaded. Name collisions keep the first discovered skill and produce a warning.

## Validate and share a skill

Run Pi from a location where the skill is discoverable, then inspect the startup diagnostics and `/skill:name` command. Run `/reload` after editing a skill during an active session.

Use a [Pi package](../03-customize-pi/05-packages.md) to distribute one or more skills through npm or git. Keep environment setup inside the skill and declare any required runtime dependencies in the package.

For examples, see the [Anthropic skills collection](https://github.com/anthropics/skills) and [Pi skills collection](https://github.com/badlogic/pi-skills).


<!-- ============================================================ -->
<!-- SOURCE: 03-customize-pi/04-themes.md -->
<!-- ============================================================ -->

# Customize Pi with themes

Themes control the colors Pi uses in interactive mode and HTML exports. Pi includes the `system`, `dark`, and `light` themes. You can select one theme, follow your terminal's light or dark appearance, or create your own palette.

## Use your terminal's colors

The `system` theme is the default. It builds Pi's colors from your terminal's theme, so Pi matches the terminal instead of bringing its own palette:

- Pi queries the terminal's default foreground and background colors and its 16 ANSI colors.
- Each Pi color takes its hue from one ANSI color, for example errors from red and links from blue.
- Pi sets each color's lightness so that it stands out from the background by a minimum contrast. Body text keeps at least a 4.5:1 WCAG contrast ratio on the background and every panel.
- When the terminal switches between light and dark, Pi queries the colors again and rebuilds the theme.

The theme adapts to what the terminal reports:

| Terminal reports | Result |
|---|---|
| Background and ANSI colors | Colors from the terminal palette, placed for the actual background. |
| Background only | Pi's own hues, placed for the actual background. |
| Nothing | ANSI color indices and the terminal's default colors, which the terminal renders itself. Secondary text is faint, and panels have no background color. |

Pi asks the terminal for its colors when it starts. Terminals usually answer within a few milliseconds, and Pi waits at most 100 ms before showing the startup header. If the terminal does not answer in time, Pi uses the ANSI color fallback, and it still applies the colors if they arrive later, for example over a slow SSH connection. `system` is a reserved name: a custom theme with that name is ignored.

<a id="selecting-a-theme"></a>

## Choose a theme

Open `/settings` and select **Theme**. You can use one theme for every terminal appearance or choose separate themes for light and dark terminals.

The selection is saved as the `theme` [setting](../05-reference/04-settings.md#terminal-and-display):

```json
{
  "theme": "dark"
}
```

Without a `theme` setting, Pi uses `system`.

Automatic mode stores the light theme first and the dark theme second:

```json
{
  "theme": "light/dark"
}
```

Pi decides whether the terminal is light or dark from its reported background and foreground colors. If the terminal does not report its background, Pi uses the terminal's light/dark notification, then the `COLORFGBG` environment variable, then dark. The same decision picks the theme of a light/dark pair and the appearance of `system`. When automatic mode is active, Pi changes themes when the terminal reports an appearance change. Theme names cannot contain `/` because Pi reserves it for this setting format.

Use `--use-theme` to choose the initial theme for one invocation without changing the saved setting:

```bash
pi --use-theme light
pi --use-theme light/dark
```

See [CLI resources](../05-reference/01-cli.md#resources) for the command-line option.

## Create a custom theme

Copy one of the [built-in themes](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/src/modes/interactive/theme) or create a new JSON file conforming to the [schema](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/modes/interactive/theme/theme-schema.json). The built-in themes use OKHSL colors, with variables for colors that several roles share, so you can adjust a hue, saturation, or lightness directly.

1. Save the file as `<agent-dir>/themes/my-theme.json`. The agent directory defaults to `~/.pi/agent`.
2. Set its `name` to `my-theme`.
3. Change values in `vars` and `colors`.
4. Select `my-theme` through `/settings`.

Use the theme name as the filename. Pi hot-reloads the active user theme only from `<agent-dir>/themes/<name>.json`. Run `/reload` after adding or changing a theme from any other source.

## Understand the theme file

| Property | Required | Responsibility |
|---|---|---|
| `$schema` | No | Enables editor validation and completion against Pi's published schema. |
| `name` | Yes | Identifies the theme in selectors and settings. It must be unique, cannot contain `/`, and cannot be `system`. |
| `appearance` | No | `"dark"` or `"light"`: the background the theme is designed for. Pi detects it from the theme colors when omitted. |
| `vars` | No | Defines reusable color values. Variables can reference other variables. |
| `colors` | Yes | Assigns colors to terminal UI roles. The schema identifies required and optional roles. |
| `export` | No | Overrides page and panel backgrounds in HTML exports. |

A color can be written in six forms:

| Form | Example | Meaning |
|---|---|---|
| RGB hexadecimal | `"#0af"` or `"#00aaff"` | A three- or six-digit sRGB color. |
| OKLCH | `"oklch(62% 0.1 200)"` | Perceptual lightness, chroma, and hue. |
| OKHSL | `"okhsl(250 60% 55%)"` | Hue, saturation, and lightness. Saturation is relative to the most the sRGB gamut allows at that hue and lightness, so every value is in gamut and equal saturation looks equally colorful. |
| 256-color index | `39` | An ANSI palette index from `0` through `255`. |
| Variable reference | `"primary"` | The value of an entry in `vars`. |
| Terminal default | `""` | The terminal's default foreground or background color. |

Terminal default colors render as the terminal's own colors. Where Pi needs a concrete value, such as HTML export or extension color math, it uses the default colors the terminal reports, or a black or white guess based on the theme's appearance.

Pi resolves chained variable references. A missing variable or circular reference makes the theme invalid. Pi uses truecolor when available, gamut-maps OKLCH to sRGB, and approximates colors for 256-color terminals. HTML exports convert OKHSL values to hexadecimal because CSS does not support them. If colors differ from their source values, check your terminal's truecolor detection and contrast settings. See [Configure Your Terminal](../02-run-pi/07-terminal-setup.md#override-detected-capabilities).

Use the [theme JSON schema](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/modes/interactive/theme/theme-schema.json) for the exact properties, required colors, and accepted value types.

Pi reports invalid theme files during startup and `/reload`.

## Find the color to change

Theme colors describe interface roles rather than individual components. Use these groups to find the relevant part of the schema:

| Area | Color names |
|---|---|
| General interface | `accent`, `border*`, `text`, `muted`, `dim`, `success`, `error`, `warning` |
| Selection and fullscreen | `selectedBg`, `searchMatch*`, `scrollbar*` |
| Messages | `userMessage*`, `customMessage*`, `thinkingText` |
| Tool execution | `toolPendingBg`, `toolSuccessBg`, `toolErrorBg`, `toolTitle`, `toolOutput` |
| Markdown | `md*` |
| Tool diffs | `toolDiff*` |
| Syntax highlighting | `syntax*` |
| Editor modes | `thinking*`, `bashMode` |
| HTML export | `export.pageBg`, `export.cardBg`, `export.infoBg` |

The schema is the format reference. The built-in themes provide complete values that you can copy and adjust.

Five colors are optional and inherit another color when omitted:

| Optional color | Fallback |
|---|---|
| `scrollbarTrack` | `muted` |
| `scrollbarThumb` | `text` |
| `searchMatchBg` | `selectedBg` |
| `searchMatchText` | `text` |
| `thinkingMax` | `thinkingXhigh` |

If `export` colors are omitted, Pi derives HTML page and panel backgrounds from `userMessageBg`.

## Load a theme from a project or package

Place a project theme in `.pi/themes/`. Project themes load only after [project trust](../02-run-pi/04-security.md#understand-project-trust) is granted.

You can also load theme files and directories through the `themes` setting or distribute them in a Pi package. See [Configuration](../03-customize-pi/01-configuration.md), [Settings](../05-reference/04-settings.md#resources), and [Pi Packages](../03-customize-pi/05-packages.md).

Each loaded theme must have a unique name. Pi reports duplicate names as resource collisions.


<!-- ============================================================ -->
<!-- SOURCE: 03-customize-pi/05-packages.md -->
<!-- ============================================================ -->

# Pi Packages

Pi packages install and distribute extensions, skills, prompt templates, and themes as one unit. Use a package when a customization should be shared through npm or git, or when several resources belong together.

A package is an ordinary directory or npm package. It can expose conventional resource directories, declare explicit paths under the `pi` key in `package.json`, and carry its own runtime dependencies.

## Install and manage packages

Install from npm, git, or a local path:

```bash
pi install npm:@example/pi-tools@1.0.0
pi install git:github.com/example/pi-tools@v1
pi install ./local-package
```

`pi list` shows configured packages. Use `pi remove <source>` to remove one and `pi update --extensions` to reconcile package installations. See [Command Line](../05-reference/01-cli.md#package-commands) for every package command and option.

Personal installs are written to `~/.pi/agent/settings.json`. Add `--local` or `-l` to write the package declaration to `.pi/settings.json`. Pi reads declarations from that file only after project trust is granted.

Project packages are installed and loaded only after project trust is resolved. Packages can execute extension code and can include skills that instruct the model to run programs. Review third-party package source before installing it. Review project package declarations before granting project trust.

Use `--extension` or `-e` to try a package for one invocation without adding it to settings:

```bash
pi -e npm:@example/pi-tools
```

## Choose a source

| Source | Example | Behavior |
|---|---|---|
| npm | `npm:@example/pi-tools@1.0.0` | Installed under the Pi npm directory |
| git | `git:github.com/example/pi-tools@v1` | Cloned and reconciled to the selected ref |
| URL | `https://github.com/example/pi-tools` | Treated as a git source |
| Local | `./pi-tools` | Loaded from the resolved path without copying |

Versioned npm specifications are pinned. Git tags and commits are also pinned; package updates reconcile the checkout but do not move a configured ref.

Relative local paths resolve from the settings file that contains them. A file path loads one extension. A directory follows normal package discovery rules.

## Create a package

The simplest package uses conventional directories:

```text
my-pi-package/
├── package.json
├── extensions/
├── skills/
├── prompts/
└── themes/
```

Without a `pi` manifest, Pi discovers TypeScript and JavaScript extensions, skill directories, Markdown prompts, and JSON themes from those directories.

Use an explicit manifest when resources live elsewhere or need filtering:

```json
{
  "name": "my-pi-package",
  "keywords": ["pi-package"],
  "pi": {
    "extensions": ["./src/extension.ts"],
    "skills": ["./resources/skills"],
    "prompts": ["./resources/prompts/*.md"],
    "themes": ["./resources/themes/*.json"]
  }
}
```

Paths are relative to the package root. Arrays accept glob patterns and exclusions. List dot-prefixed or symlinked resource roots directly when traversal through a glob would not discover them.

The `pi-package` keyword makes an npm package eligible for discovery in the [Pi package gallery](https://pi.dev/packages). Optional `pi.image` and `pi.video` fields add gallery previews.

## Declare dependencies

Put runtime packages imported by extensions in `dependencies`. Pi installs package dependencies when it installs an npm or git source.

Pi supplies these packages to extensions and skills:

- `@earendil-works/pi-ai`
- `@earendil-works/pi-agent-core`
- `@earendil-works/pi-coding-agent`
- `@earendil-works/pi-tui`
- `typebox`

Declare the host-provided packages listed above in `peerDependencies` with a `"*"` range and do not bundle them. Pi suppresses automatic peer installation for managed npm packages and git packages installed with npm, pnpm, or Bun. Local packages are not installed or modified, so their dependency tree remains the package author's responsibility.

Do not list host-provided packages in `dependencies`. A physical copy can bypass Pi's extension module mapping in compiled ESM and create duplicate classes, registries, and initialization work. Pi reports an extension warning when it detects this manifest configuration. Other Pi packages used as dependencies must be included in the published tarball and referenced through their `node_modules` resource paths.

Installed packages load with separate module roots. Do not rely on two packages sharing one dependency instance or one package resolving another package’s undeclared dependency.

## Select package resources

The object form in settings narrows which resources load from a package:

```json
{
  "packages": [
    {
      "source": "npm:@example/pi-tools",
      "extensions": ["extensions/*.ts", "!extensions/legacy.ts"],
      "skills": [],
      "prompts": ["prompts/review.md"]
    }
  ]
}
```

For each resource type:

- Omit the property to load everything allowed by the package.
- Use `[]` to load none of that type.
- Use `!pattern` to exclude glob matches.
- Use `+path` to include one exact allowed path.
- Use `-path` to exclude one exact path.

Filters narrow the package manifest. They do not expose resources that the package itself did not declare.

Run `pi config` to enable or disable discovered resources and pi's built-in extensions. It starts with personal configuration; press Tab to switch scope, or run `pi config --local` to start with project overrides.

## Understand scope and identity

The same package can appear in personal and project settings. A project entry normally replaces the personal entry. With `autoload: false`, the project entry instead acts as a filtering delta over the personal package.

Pi identifies npm packages by package name, git packages by repository URL without the ref, and local packages by resolved absolute path. This prevents the same package from loading twice through equivalent declarations.

Use [Extensions](../04-build-on-pi/01-extensions.md), [Skills](../03-customize-pi/03-skills.md), [Prompt Templates](../03-customize-pi/02-prompt-templates.md), and [Themes](../03-customize-pi/04-themes.md) to design each resource before packaging it.


<!-- ============================================================ -->
<!-- SOURCE: 03-customize-pi/06-mcp.md -->
<!-- ============================================================ -->

# MCP Servers

Pi connects to [Model Context Protocol](https://modelcontextprotocol.io) servers over stdio or streamable HTTP and makes their tools and resources available to the model.

## Quick setup

Add a local stdio server, check the connection, then start Pi:

```bash
pi mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem .
pi mcp list
pi
```

For a remote server:

```bash
pi mcp add docs --url https://example.com/mcp --bearer-token-env-var DOCS_TOKEN
pi mcp list
```

These commands add user-level servers by default. Add `--local` or `-l` to write the project configuration instead:

```bash
pi mcp add -l tools --env API_KEY='${TOOLS_KEY}' -- uvx tools-mcp
```

Use `/mcp` inside an interactive session to inspect connections, sign in, reconnect, change exposure, or enable and disable servers. Run `/reload` after adding, removing, or changing a server outside the session.

## Configure servers

Pi reads user-level servers from `~/.pi/agent/mcp.json` and project servers from `.pi/mcp.json`. Project configuration is read only after [project trust](../02-run-pi/04-security.md#understand-project-trust) is granted. A project entry replaces a user-level entry with the same name.

A project entry without `command`, `url`, or `type` overrides only `enabled`, `exposure`, and `toolExposure` of the user-level server with the same name and keeps the rest, including `env`, `headers`, and `auth`. For example, this turns off a user-level server in one project:

```json
{
  "mcpServers": {
    "internal-tools": { "enabled": false }
  }
}
```

The format matches other MCP clients:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "docs": {
      "url": "https://example.com/mcp",
      "headers": { "Authorization": "Bearer ${DOCS_TOKEN}" },
      "description": "Search and read the product documentation"
    }
  }
}
```

Stdio servers use `command`, `args`, `env`, and `cwd`. Relative `cwd` values resolve against the session directory. A leading `~/` in `command`, an argument, or `cwd` names the home directory.

HTTP servers use `url`, `headers`, and `oauth` (see [Authenticate with OAuth](#authenticate-with-oauth)). The legacy SSE transport is not supported.

Both server types support:

- `timeout`: per-request timeout in seconds (default 60). Progress notifications reset it.
- `enabled: false`: keep the entry without connecting to it.
- `exposure` and `toolExposure`: control how tools reach the model (see [Control tool exposure](#control-tool-exposure)).
- `description`: what the server offers, in a sentence. It lists the server in the system prompt (see [Control tool exposure](#control-tool-exposure)), tool search ranks the server's tools by it, and codemode's `describeNamespace()` returns it. Without it, the first line of the server instructions is used once the server connects.

Keep personal servers and servers with credentials in the user-level file. Use the project file only for servers the project requires, and only in trusted projects.

### Configuration rules

- Server names may contain only letters, digits, `_`, and `-`. Tools are named `mcp__<server>__<tool>`, with every character other than letters, digits, and `_` replaced by `_`; tools of a server whose names then collide all get a hash suffix. Server names that differ only in `-` and `_` count as the same server: a second one is rejected, and a `mcp.json` server overrides a registered one.
- `type` is optional. A `command` selects stdio and a `url` selects streamable HTTP. When present, `type` must be `stdio`, `http`, or `streamable-http`.
- `sse` is rejected. Servers that document an SSE endpoint often also provide streamable HTTP, commonly at `/mcp` instead of `/sse`.
- `command` is one executable and `args` contains its arguments. It is not a shell command string.
- `env` and `headers` values can use environment variables such as `${GITHUB_TOKEN}`. They can also run a command with `!command`, but the command must make up the whole value, for example `"Authorization": "!echo Bearer $(gh auth token)"`.
- Invalid entries are reported and skipped without preventing other servers from connecting.

`pi mcp add` and `pi mcp remove` cover common changes from a shell. See [MCP commands](../05-reference/01-cli.md#mcp-commands) for their options.

### Inspect or change a server

`/mcp` lists configured servers with their state, tool count, exposure, and configuration source. Servers that need attention appear first. Select a server to inspect its tools and connection details, reconnect, sign in or out, change exposure, or enable and disable it.

Exposure and enabled-state changes are saved to the file that defines the server without replacing unrelated content. In a trusted project, "Enable in this project" and "Disable in this project" add a project override for a user-level server; later changes to that server are saved to the override. Disabled servers remain listed. Outside the interactive TUI, `/mcp` prints server status; `/mcp login <server>`, `/mcp logout <server>`, and `/mcp reconnect <server>` perform those actions directly.

Shell commands work without a session: `pi mcp add`, `pi mcp remove`, `pi mcp list`, `pi mcp login`, and `pi mcp logout`. Shell commands do not load extensions.

### Diagnose connection problems

Run `pi mcp list` to connect to every enabled server and print its state, tools, and errors. It exits with status 1 when an entry is invalid or an enabled server is not connected. `/mcp` shows the full connection error and the tail of stderr from a failed stdio server.

Pi reports configuration errors, failed connections, and required sign-ins once after startup. Server logging notifications are appended to `~/.pi/agent/mcp.log` as `<time> [<server>] <level> <logger>: <message>`. The file moves to `mcp.log.1` after it grows past 5 MB.

Pi connects every enabled server in the background when a session starts. A server's tools appear once it connects; the `codemode` description does not list them, so it does not change when servers connect. The first prompt waits up to 10 seconds only for servers with `direct` tools, which must be declared in its request. Other servers are waited for when they are needed: a codemode script waits for the servers it names (`mcp__<server>`) and, when it calls `searchTools()` or reads `ALL_TOOLS`, for all of them; `tool_search` and the resource tools also wait for all of them. HTTP network errors and transient statuses (408, 429, and 5xx) are retried twice. A dropped connection is shown as disconnected and reconnects on the next call. When a server announces a changed tool list, new tools are added and withdrawn tools become unreachable.

Stopping a stdio server closes its stdin, sends SIGTERM, then sends SIGKILL to its process group. This also stops servers launched through wrappers such as `npx` or `uvx`.

## Migrate configuration from another client

Move the converted entry under `mcpServers` in `mcp.json`, then run `pi mcp list` to validate it.

| Client | Conversion |
|---|---|
| Claude Desktop, Claude Code, or Cursor | Copy the existing `mcpServers` entry. |
| VS Code | Move an entry from the top-level `servers` object and replace `${input:...}` prompts with `${NAME}` environment variables. |
| Codex | Convert `[mcp_servers.<name>]` TOML fields such as `command`, `args`, `env`, and `url` to JSON. |
| OpenCode | Convert `"type": "local"` to a stdio entry, split its `command` array into `command` and `args`, rename `environment` to `env`, and replace `{env:NAME}` with `${NAME}`. Convert `"type": "remote"` to a URL entry. |

## Authenticate with OAuth

Remote servers that use OAuth, such as Sentry, need no credentials in `mcp.json`:

```json
{
  "mcpServers": {
    "sentry": { "url": "https://mcp.sentry.dev/mcp" }
  }
}
```

When the server rejects an unauthenticated connection, `/mcp` shows that it needs sign-in. Select "Sign in", run `/mcp login sentry`, or run `pi mcp login sentry`. Pi opens the authorization page and waits for approval. If the browser runs on another machine, such as over SSH, paste its redirected URL into the sign-in screen. A running session uses the new credentials on its next turn.

Pi registers itself with the authorization server, stores tokens in `~/.pi/agent/mcp-auth.json`, and refreshes access tokens when they expire or the server rejects them. If a server later requests additional scope, Pi asks for sign-in again. Signing out deletes the stored credentials.

Credentials belong to a server name and URL. Servers with the same URL under different names, such as one per account, sign in separately; servers with the same name and URL in different `mcp.json` files share one sign-in.

OAuth applies to HTTP servers without an `Authorization` header. For a server that does not support dynamic client registration, configure a registered client:

```json
{
  "mcpServers": {
    "example": {
      "url": "https://mcp.example.com/mcp",
      "oauth": { "clientId": "my-client", "clientSecret": "${EXAMPLE_SECRET}", "callbackPort": 8765 }
    }
  }
}
```

The redirect URI must match the registered URI. `callbackPort` uses `http://127.0.0.1:<port>/callback`. To use another URI, set `callbackUrl`; it must use HTTP on `localhost`, `127.0.0.1`, or `[::1]`. Pi sends it exactly as written. When `callbackUrl` omits a port, Pi uses `callbackPort` or a free port and adds it to the URI, as allowed for loopback redirects by RFC 8252. `clientSecret` is optional and can use an environment variable or command.

Set `scope` to a space-separated list for servers that do not advertise their required scopes. Otherwise, Pi requests the advertised scopes. Later scope requests are added to the configured value.

Pi registers as `pi`. Some servers only accept registrations from known clients. Set `clientName` to send another name:

```json
{
  "mcpServers": {
    "figma": { "url": "https://mcp.figma.com/mcp", "oauth": { "clientName": "Claude Code" } }
  }
}
```

The name is only sent when Pi registers a client. To register again under a new name, sign out first.

Some authorization servers allow clients by their Client ID Metadata Document URL instead of registering them. Set `clientRegistration` to `cimd` to identify as Pi's document on pi.dev instead of registering:

```json
{
  "mcpServers": {
    "example": { "url": "https://mcp.example.com/mcp", "oauth": { "clientRegistration": "cimd" } }
  }
}
```

The client ID is `https://pi.dev/oauth/client.json` with the redirect URI `http://127.0.0.1:<port>/callback`. If the authorization server does not send the `iss` parameter in authorization responses (RFC 9207), Pi uses a document and redirect path specific to the MCP server instead: `https://pi.dev/oauth/<id>/client.json` with `http://127.0.0.1:<port>/callback/<id>`. The authorization server must advertise Client ID Metadata Document support and public clients, or sign-in fails. `cimd` cannot be combined with `clientId` or `clientName`, and a `callbackUrl` must use `localhost` or `127.0.0.1` with the path `/callback`.

Pi finds the authorization server through the server's protected resource metadata (RFC 9728) and checks that the authorization server's metadata names the expected issuer (RFC 8414). Some servers advertise the wrong authorization server or none, so sign-in opens a page that does not exist. Set `authServerMetadataUrl` to the metadata document of the right authorization server:

```json
{
  "mcpServers": {
    "example": {
      "url": "https://mcp.example.com/mcp",
      "oauth": { "authServerMetadataUrl": "https://example.okta.com/.well-known/openid-configuration" }
    }
  }
}
```

Pi uses that document instead of discovery and trusts it as configured, so only point it at a document you trust. The URL must use HTTPS, except on `localhost`, `127.0.0.1`, or `[::1]`.

## Control tool exposure

Each server tool is registered as `mcp__<server>__<tool>`. The server's `exposure` determines how the model reaches it:

| Exposure | Behavior | Typical use |
|---|---|---|
| `codemode` (default) | Callable from [`codemode`](../05-reference/01-cli.md#tools) scripts, but neither declared to the model nor listed in the codemode description. Scripts find tools with `searchTools()`, `describeTool()`, or `ALL_TOOLS`. | General MCP servers, especially when scripts should combine or filter calls. |
| `deferred` | Not declared until [`tool_search`](../05-reference/01-cli.md#tools) loads a match for the next model call. | Large servers whose tools should be called directly after discovery. |
| `direct` | Declared to the model like a built-in tool and also callable from codemode. | Small, frequently used tool sets. |
| `hidden` | Registered but unreachable. | Servers or tools that should remain unavailable. |

`codemode-deferred` is accepted as an alias for `codemode`.

Servers with `codemode` or `deferred` tools are listed in the `mcp_servers` section of the system prompt, with how their tools are reached and one line from the configured `description` or, once connected, from the server instructions. Pi updates the section when a prompt starts, after waiting for servers with `direct` tools. When it changed, for example because a server connected and its summary became available, Pi appends the new section to the conversation instead of changing tool declarations, so earlier messages stay cached. `describeNamespace()` and the `namespace` option of `searchTools()` accept `mcp__dev-radius`, `mcp__dev_radius`, `dev-radius`, or `dev_radius`.

Pi activates `codemode` when a server with `codemode` exposure connects. It activates `tool_search` for a server with `deferred` exposure. To make the model see a tool without searching, give it `direct` exposure with `toolExposure`.

`toolExposure` overrides the server exposure for individual tools. Keys are exact server tool names or patterns where `*` matches any characters. Exact names win over patterns; among patterns, the first match wins. A server with `hidden` exposure can expose only selected tools:

```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "exposure": "deferred",
      "toolExposure": {
        "search_code": "direct",
        "get_*": "codemode",
        "delete_*": "hidden"
      }
    }
  }
}
```

`pi mcp list` marks tools whose exposure differs from their server. The Tools view in `/mcp` also shows the effective exposure.

Tools with `codemode` or `deferred` exposure can be reached through either indirect mechanism: codemode scripts can call them, and `tool_search` can load them. Codemode calls do not depend on the active tool set, so they remain available after `/tree`, resume, and fork. Tools loaded by `tool_search` are recorded in the transcript and remain declared on that branch.

To keep `codemode` active without MCP servers, add `"defaultTools": ["+codemode"]` to [settings](../05-reference/04-settings.md#tools). To prevent automatic codemode activation, set `"autoEnableCodemode": false` beside `mcpServers`. A project value overrides the user-level value. Pi warns once when neither `codemode` nor `tool_search` is active and non-direct tools cannot be called.

Text results over 20 KB reach the model with their middle removed around a `…N chars truncated…` marker. The full text is saved to a temporary file named in the result. Codemode scripts receive the complete result and can reduce it before returning output to the model.

Codemode scripts receive the complete MCP `CallToolResult`, including `content`, `structuredContent`, and `isError`. A result with `isError` resolves inside scripts but is reported as an error for direct calls. `image(result.content[0])` forwards an image block. Server instructions are not part of any tool description; scripts read them with `describeNamespace("mcp__<server>")`, which also returns the server's tool names.

## Use resources

When a connected server offers [resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources), Pi adds the resource tools used by Codex and OpenCode:

- `list_mcp_resources` lists resources as JSON: `{ server?, resources: [{ server, uri, name, ... }], nextCursor? }`. With `server`, it lists one page; `cursor` continues with the next page. Without `server`, it lists every resource from every server.
- `list_mcp_resource_templates` lists URI templates for resources the servers do not list directly.
- `read_mcp_resource` reads a resource by `server` and `uri`. Text reaches the model as text and images as images. Other binary resources are saved to temporary files, and the model receives the path. Scripts receive `{ server, uri, contents }`.

These tools reach every enabled, non-hidden server with resources. Their exposure is the widest exposure among those servers: `direct`, then `codemode` or `deferred`. Resource links in tool results identify `read_mcp_resource` and the server.

Resources for MCP Apps, identified by `ui://` URIs or `text/html;profile=mcp-app`, are omitted because Pi does not render them. Resource icons are also omitted.

Reading and listing resources is retried once after a transient HTTP error (408, 429, or 5xx). Tool calls are not retried because the server may already have performed them.

## Permissions

Every MCP call passes through Pi's tool pipeline. Extension `tool_call` and `tool_result` handlers, including permission gates, therefore apply to MCP tools. Calls made from codemode scripts carry the codemode call ID as `parentToolCallId`.

`pi.getAllTools()` reports the annotations declared by each server: `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint`. Permission extensions can use these hints to decide which calls require confirmation (see [Tool exposure](../04-build-on-pi/01-extensions.md#tool-exposure)). Resource tools are marked read-only.

## Extensions and SDK

### Add servers from extensions

Extensions can add servers for the current session with `pi.registerMcpServer(name, config)`, using the same shape as an `mcpServers` entry (see [MCP servers in extensions](../04-build-on-pi/01-extensions.md#mcp-servers)). Registered servers connect like configured servers and appear in `/mcp` with the extension as their source.

Changes to enabled state or exposure apply only to the current session. A file-configured server with the same name takes precedence, and `/mcp` lists the overridden registration. `pi mcp` shell commands do not load extensions and only see file-configured servers.

### Replace the built-in MCP support

An installed extension that registers `/mcp`, such as `pi-mcp-adapter`, replaces the built-in MCP support for sessions. Pi then does not read `mcp.json` or connect its servers in a session, and `/mcp` belongs to the extension. Remove the extension to restore the built-in behavior. To disable built-in MCP support without a replacement, disable `mcp` under Built-in in `pi config`, or set `"extensions": ["-builtin:mcp"]` in [settings](../05-reference/04-settings.md#resources).

An extension that registers `codemode` or `tool_search` similarly replaces the built-in tool with that name. Shell-level `pi mcp` commands always use the built-in implementation.

### Use MCP from the SDK

SDK sessions do not load built-in extensions. Add the MCP extension, the codemode extension for `codemode` servers, and the tool-search extension for `deferred` servers to the resource loader. See [Codemode and MCP](../04-build-on-pi/06-sdk.md#codemode-mcp).


<!-- ============================================================ -->
<!-- SOURCE: 04-build-on-pi/01-extensions.md -->
<!-- ============================================================ -->

# Extensions

Extensions are TypeScript modules that add executable behavior to Pi. Use one when a workflow needs tools, commands, event handlers, model providers, session state, or terminal UI rather than instructions alone.

An extension runs inside the Pi process with the same operating-system permissions. It can inspect prompts, tool calls, files, credentials, and session history, so load extensions only from sources you trust.

Typical extensions add an agent tool, protect paths, confirm dangerous commands, react to session events, modify context, expose a command, or display persistent status.

<a id="quick-start"></a>
<a id="writing-an-extension"></a>
<a id="create-an-extension"></a>

## Create and load an extension

An extension exports a default factory that receives `ExtensionAPI`. The factory registers capabilities for the current extension runtime.

Create `~/.pi/agent/extensions/hello.ts`:

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerCommand("hello", {
    description: "Show a greeting",
    handler: async (name, ctx) => {
      ctx.ui.notify(`Hello, ${name || "world"}!`, "info");
    },
  });
}
```

Start Pi and run `/hello`. During development, load a file directly:

```bash
pi --extension ./hello.ts
```

Pi uses `jiti`, so local TypeScript extensions do not need a separate compilation step. Use [Pi packages](../03-customize-pi/05-packages.md) for distributed extensions and dependencies.

<a id="extension-locations"></a>
<a id="available-imports"></a>
<a id="choose-where-it-loads"></a>

## Add it to Pi

Place the extension in your user or project extensions directory. Pi loads direct TypeScript or JavaScript files and subdirectories containing an `index.ts` or `index.js` entry point.

Use a single file for a small extension and a directory for a multi-file implementation. Put npm dependencies in a nearby `package.json`. See [Configuration](../03-customize-pi/01-configuration.md) for conventional locations and [Settings](../05-reference/04-settings.md#resources) for additional paths.

Reload replaces the extension runtime, so code after `await ctx.reload()` must not reuse state from the old runtime. Only personal and explicit command-line extensions can participate in the `project_trust` event that runs before project extensions load.

<a id="understand-the-lifecycle"></a>

## Respect the runtime lifecycle

The factory can be synchronous or asynchronous. Pi waits for an asynchronous factory before startup continues, allowing it to fetch configuration or register providers needed during startup.

Do not start processes, sockets, watchers, or timers in the factory because some invocations load extensions without starting a session.
Start long-lived resources from `session_start` or from the command or tool that needs them.
Close session-scoped resources from an idempotent `session_shutdown` handler.

A run proceeds from input and `before_agent_start`, through model, message, and tool events, to `agent_end`.
Automatic retries, recovery, compaction, or queued work can continue afterward.
<a id="agent_start--agent_end--agent_before_settle--agent_settled"></a>

`agent_before_settle` is the final actionable boundary: it can append entries and request one continuation.
`agent_settled` is final and notification-only; use it when an integration needs to know Pi will not continue automatically.

<a id="extensionapi-methods"></a>

## Choose an integration point

| Capability | Main API |
|---|---|
| Observe or modify lifecycle behavior | `pi.on()` |
| Add a model-callable operation | `pi.registerTool()` |
| Add a `/` command | `pi.registerCommand()` |
| Add a shortcut or CLI flag | `pi.registerShortcut()` or `pi.registerFlag()` |
| Send user or custom messages | `pi.sendUserMessage()` or `pi.sendMessage()` |
| Persist non-context session data | `pi.appendEntry()` |
| Change active tools, model, or thinking level | Session control methods on `pi` |
| Add a model provider | `pi.registerProvider()` |
| Add an MCP server | `pi.registerMcpServer()` |
| Route each request to a model | [`pi.registerVirtualModel()`](../04-build-on-pi/03-virtual-models.md) |
| Add terminal rendering | Renderer registration and `ctx.ui` |
| Communicate with another extension | `pi.events` |

Use the exported declarations in [`extensions/types.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/extensions/types.ts) for exact event, context, tool, and result types.

## Follow the extension contracts

<a id="events"></a>
<a id="work-with-events"></a>

### Events and concurrency

Handlers run in extension load and registration order. `pi.on()` returns a function that unsubscribes that registration; changes do not affect a dispatch already in progress.
Some events notify; others transform data, replace results, or cancel an operation.
Use each event’s declared result type rather than assuming every return value has an effect.

Events cover resource discovery, sessions, agent and message lifecycle, providers, tools, and raw input.

`before_agent_start` exposes both the current prompt and its structured `systemPromptOptions`. Prefer changing prompt sections, selected tools, or guidelines so Pi can append a transcript delta. Returning `systemPrompt`, or setting `forceSystemPrompt`, replaces the whole prompt for that run while the transcript continues recording the structured sections. Providers receive the forced text as their leading system prompt.

`message_end` can replace a finalized message while preserving its role. `tool_call` can mutate input or block execution. `tool_result` handlers compose, with each handler seeing prior changes.

<a id="provider_stream_event"></a>

`provider_stream_event` fires for each parsed provider stream event before Pi normalizes it. The event identifies the provider, API, and model; `event.data` is the earliest structured value available to Pi, not necessarily the original HTTP bytes or SSE frame. Treat it as read-only because mutation can affect normalization. The event is notification-only and is not persisted.

Handlers are awaited in stream order, so slow handlers delay stream consumption. Handler errors are reported without changing the provider response. See [`debug-provider.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/debug-provider.ts) for an opt-in viewer that groups raw events by assistant message.

<a id="context_with_system"></a>

`context` transforms conversation messages without prompt and tool system messages; Pi restores that state afterward. Use `context_with_system` only when a request-local transformation must own the complete transcript, and keep a system message at index zero.

`turn_end` and `agent_before_settle` are actionable boundaries. Their handlers can chain proposed `custom`, `custom_message`, `context_edit`, or `compaction` entries and return `continue: true` for one next model request. Guard continuation conditions because an unconditional continuation can loop. Use the exported event declarations for the complete validation and ordering contract.

<a id="cache_warming_decision"></a>

`cache_warming_decision` can override an idle prompt-cache refresh with `{ action: "warm" }` or `{ action: "stop" }`. The last handler that returns an action wins.

Tool calls from one assistant message can run in parallel.
Do not assume a sibling call or result exists when another tool event runs.
Use `ctx.signal` for nested work owned by an active turn; commands and idle session events often have no operation signal.

A `user_bash` handler that returns `undefined` passes the command to the next handler and then to local execution if no handler handles it. Returning `operations` or `result` stops propagation. A handler failure blocks the command rather than falling through to local execution.

<a id="custom-tools"></a>
<a id="register-tools"></a>

### Tools

A custom tool defines a name, model-facing description, TypeBox parameter schema, and `execute()` function.
Its result requires model-facing `content` and a `details` field for rendering or state reconstruction.
Use `details: undefined` when there are no structured details. If the tool makes nested model calls, include their `usage` in the result so session totals remain accurate.

Throw from `execute()` to produce a failed tool result.
Returning an object does not mark it as an error.
Return `terminate: true` only when the agent should skip its automatic follow-up after every completed tool in that batch agrees to terminate.

Use sequential execution when tools share mutable in-memory state.
File-mutating tools should wrap the complete read-modify-write operation with `withFileMutationQueue()`.
Truncate large model-facing results and tell the model where to read the complete output.

Declare `outputSchema` and return a matching `structuredContent` when the result is data. The model still receives `content`; programmatic callers such as codemode scripts receive `structuredContent` instead of the text. Tools without `outputSchema` are passed to scripts as their text content. To report a failure that still carries data, return the result with `isError: true` instead of throwing: the model sees an error, and scripts still receive `structuredContent`.

A tool can run other tools with `ctx.executeTool(name, args, { signal, onUpdate })`. Nested calls go through argument validation and the `tool_call` and `tool_result` handlers like model-issued calls, and emit `tool_execution_start`, `tool_execution_update`, and `tool_execution_end`; all of these events carry `parentToolCallId`, and their `toolCallId` is assigned by pi as `<parent id>/<n>`. These ids do not appear as tool calls or tool results in the transcript. Nested calls do not add transcript entries: their results only reach the calling tool, which reports them itself, for example through `onUpdate` and `details`. The session keeps a bounded record of them (name, arguments, status, duration, error; never results) as `nestedCalls` on the calling tool's result message. It is used for compaction file lists and shown in HTML exports. Arguments over 8 KiB per call or 32 KiB per tool result are omitted, at most 256 calls are kept, and `complete: false` marks a record that lost anything. The `usage` of nested results, at every depth, is added to the calling tool's result `usage`, so a tool reports only its own usage, not that of the tools it called. `ctx.tools` lists the tools `ctx.executeTool()` can call. `tool_result` handlers that redact `content` should also replace `structuredContent`; replacing only `content` drops it.

See [`hello.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/hello.ts), [`todo.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/todo.ts), [`dynamic-tools.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/dynamic-tools.ts), and [`truncated-tool.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/truncated-tool.ts).

### Tool exposure

`exposure` controls how the model reaches a tool. "Callable" means callable from other tools through `ctx.executeTool()` (`ctx.tools`), as the `codemode` tool's scripts do:

- `direct` (default): declared to the model while active, and callable while active.
- `model-only`: declared to the model while active, never callable. Use it for tools that orchestrate other tools or ask the user.
- `codemode`: callable whenever registered, and listed by the `codemode` tool. Not declared to the model unless activated explicitly.
- `deferred`: like `codemode`, but codemode tools do not list it; `tool_search` can find and activate it.
- `hidden`: registered but unreachable. Re-register a tool with `exposure: "hidden"` to withdraw it, since tools cannot be unregistered.

`namespace: { name, description, instructions }` groups related tools, as MCP servers do. Codemode tools list a namespace under one heading with its `description`. `instructions` holds longer usage guidance; it is not listed, and codemode scripts read it with `describeNamespace(name)`.

Registering a `direct` or `model-only` tool activates it; the other exposures are not activated on registration. The active set (`pi.getActiveTools()`, `pi.setActiveTools()`) is the set of tools declared to the model. `pi.getAllTools()` reports each tool's `exposure`, `namespace`, and `annotations`.

`annotations` are hints about what a tool does, with the meaning of MCP tool annotations: `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint`. MCP tools carry the hints their server declares. Missing hints take the MCP defaults: a tool is not read-only, and may be destructive and reach an open world. The hints are not verified, but a permission extension can use them to decide which calls to confirm. This confirms the calls Codex asks approval for:

```typescript
pi.on("tool_call", async (event, ctx) => {
  const hints = pi.getAllTools().find((tool) => tool.name === event.toolName)?.annotations;
  const needsApproval =
    hints?.destructiveHint === true ||
    (!hints?.readOnlyHint && ((hints?.destructiveHint ?? true) || (hints?.openWorldHint ?? true)));
  if (needsApproval && !(await ctx.ui.confirm("Allow tool call?", event.toolName))) {
    return { block: true, reason: `${event.toolName} was not approved` };
  }
});
```

A tool that orchestrates other tools can adjust what the model sees while it is active with `prepareLoadout(loadout)`. It runs whenever the active tools change and receives the declared tools, the callable tools, and every registered tool with its exposure and namespace. It returns replacement `descriptions` for declared tools (including its own) and `hiddenDeclarations`: active tools whose declarations requests leave out while they stay active and callable. `codemode` uses only this hook, `exposure`, and `ctx.executeTool()`, so another tool can implement the same behavior under a different name.

### Activate tools dynamically

Register every tool first, keep optional tools inactive, and use `pi.setActiveTools()` from a loader tool to select the desired active tools. Names must already be registered; unknown names are ignored.

Pi records the initial prompt and tool set in the transcript's first system message, then appends tool and prompt changes before the next model request. Providers that cannot represent the transition receive a complete transcript checkpoint, which can invalidate the cached prefix.

### Tool rendering

A tool's `renderCall` and `renderResult` draw its calls in the interactive transcript and in HTML exports. `pi.registerToolRenderer((toolName, next) => renderers)` chooses renderers for calls to any tool, including tools that are not registered yet, such as MCP tools in a resumed session before their server connected. `next()` returns what the remaining resolvers (in extension load order), then the registered tool, would use, so `next() ?? mine` only fills in.

### MCP servers

`pi.registerMcpServer(name, config)` adds an MCP server for the current session. `config` has the shape of an `mcpServers` entry in [`mcp.json`](../03-customize-pi/06-mcp.md): `command`, `args`, `env`, and `cwd` for stdio servers, `url`, `headers`, and `oauth` for HTTP servers, plus `exposure`, `toolExposure`, `description`, `enabled`, and `timeout`.

```typescript
pi.registerMcpServer("jira", { url: "https://mcp.example.com/jira", exposure: "codemode" });
pi.unregisterMcpServer("jira");
```

Servers registered while the extension loads connect when the session starts, together with the `mcp.json` servers; servers registered later connect right away, and `pi.unregisterMcpServer()` closes the connection and makes the server's tools unreachable. Registrations are not saved: register again on every load, for example based on the extension's own settings. A server in `mcp.json` with the same name takes precedence, and `/mcp` shows the override. Registering the same name again replaces the extension's earlier registration; names registered by another extension, invalid names, and invalid configs throw.

The built-in MCP support connects registered servers. When nothing does, because another extension replaced it (see [MCP](../03-customize-pi/06-mcp.md#other-mcp-extensions)), each registration is reported as an extension error. Other MCP extensions can connect registered servers too: read them with `pi.getMcpServers()` on `session_start` and handle the `mcp_servers_change` event for later changes.

<a id="extensioncontext"></a>
<a id="extensioncommandcontext"></a>
<a id="use-extension-context"></a>

### Context and session changes

`ExtensionContext` provides the working directory, mode, UI, session manager, model runtime, abort signal, context usage, and controls for compaction and shutdown.
Use `ctx.modelRegistry.streamSimple()` for provider-neutral nested model calls.

Command handlers receive `ExtensionCommandContext`, which adds operations for waiting until idle, reloading, tree navigation, and session replacement.
These operations are command-only because calling them from lifecycle handlers can deadlock the runtime.

Session replacement invalidates the old context. Capture only plain data before switching, then use the fresh context supplied to `withSession` for session-bound work.

<a id="state-management"></a>
<a id="persist-state"></a>

### State

Choose storage based on how state participates in the conversation:

| State | Storage |
|---|---|
| Tool state that follows the active branch | Tool-result `details` |
| Durable data excluded from model context | `pi.appendEntry()` |
| Custom content stored and sent to the model | `pi.sendMessage()` |
| Data outside one session | External storage |

Reconstruct branch-sensitive state from `ctx.sessionManager.getBranch()` during `session_start`.
Do not rebuild it from every file entry because abandoned branches represent alternative histories.
Register an entry or message renderer when custom stored content should appear in the transcript.

<a id="custom-ui"></a>
<a id="mode-behavior"></a>
<a id="interact-with-the-user"></a>
<a id="account-for-each-mode"></a>

### UI and modes

`ctx.ui` provides dialogs, notifications, status text, widgets, titles, editor access, and custom components.
Use `ctx.ui.custom()` only when the interaction needs its own rendering and input.
See [Terminal UI](../04-build-on-pi/04-tui.md) for component, focus, overlay, theme, and performance guidance.

Extensions load in interactive, RPC, JSON, and print modes.
Interactive mode provides the complete terminal UI.
RPC can forward supported dialogs and notifications through the [RPC Extension UI protocol](../05-reference/13-rpc-extension-ui.md), but not custom terminal components; JSON and print modes have no UI.
Guard terminal-only behavior with `ctx.mode === "tui"` and use `ctx.hasUI` for interactions supported by interactive and RPC clients.

Keep tool and event behavior independent from rendering so non-interactive modes remain functional.

<a id="error-handling"></a>
<a id="handle-errors-and-shutdown"></a>

### Errors and cleanup

Pi reports handler errors and continues where possible. A `tool_call` handler failure blocks the tool as a fail-safe; a tool execution failure becomes an error result for the model.

Release resources in `session_shutdown` even when normal operation attempted cleanup.
Keep cleanup idempotent because cancellation, reload, session replacement, and process exit can converge on the same path.
Use `ctx.shutdown()` to request an orderly process shutdown.

<a id="examples-reference"></a>
<a id="use-examples-as-the-implementation-reference"></a>

## Examples and reference

The checked [extension examples](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/) cover tools, lifecycle events, commands, flags, shortcuts, state, rendering, providers, OAuth, remote execution, and terminal components.
Start with the smallest example matching your integration point.

Use [Custom Providers](../04-build-on-pi/02-custom-provider.md) for model-service integrations, [Terminal UI](../04-build-on-pi/04-tui.md) for custom components, and [Pi Packages](../03-customize-pi/05-packages.md) to install or distribute extensions with other resources.


<!-- ============================================================ -->
<!-- SOURCE: 04-build-on-pi/02-custom-provider.md -->
<!-- ============================================================ -->

# Custom Providers

A provider extension connects Pi to a model service that needs custom authentication, model discovery, request handling, or streaming. If the service already speaks a supported API, configure it in `models.json` instead.

Provider extensions run inside Pi and can inspect credentials, prompts, tool definitions, model responses, and usage. Treat them as trusted code and avoid logging secrets or provider payloads.

## Choose the smallest integration

| Requirement | Use |
|---|---|
| Add models behind a supported API | [`models.json`](../02-run-pi/02-models.md#configure-a-compatible-endpoint) |
| Change an existing provider endpoint or headers | `models.json` or a small provider extension |
| Discover models dynamically | A provider with `refreshModels` |
| Add a `/login` flow | A provider with native or legacy OAuth configuration |
| Implement an unsupported wire protocol | A provider with `stream` or `streamSimple` |

A provider extension is an [extension](../04-build-on-pi/01-extensions.md), so it follows the same loading, trust, reload, and error behavior.

## Register a provider

Call `pi.registerProvider()` from the extension factory. Pi waits for asynchronous factories before startup continues, so providers registered there are available to startup model selection and `pi --list-models`.

There are two registration forms:

- Register a complete `Provider` from `@earendil-works/pi-ai` for native authentication, filtering, discovery, refresh, and streaming behavior.
- Register a provider name with `ProviderConfig` for the legacy configuration form used by existing extensions.

Prefer a complete provider for new integrations that own more than static endpoint and model metadata. Pi composes `models.json` overrides above a registered native provider.

Registering only `baseUrl` or `headers` for an existing provider preserves its built-in models. Supplying `models` in the legacy form replaces that provider's models across chat, image, and classifier operations. An omitted `type` means `"chat"`; image and classifier models require explicit discriminants and implementations keyed by their `api` values through the `images` and `classifiers` fields.

For example, a mixed-operation provider can register non-chat models and their implementations together:

```typescript
pi.registerProvider("media-tools", {
  apiKey: "$MEDIA_TOOLS_API_KEY",
  models: [
    {
      type: "image",
      id: "image-v1",
      name: "Image V1",
      api: "media-images",
      baseUrl: "https://media.example.com/v1",
      input: ["text"],
      output: ["image"],
      cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    },
    {
      type: "classifier",
      id: "classifier-v1",
      name: "Classifier V1",
      api: "media-classifier",
      baseUrl: "https://media.example.com/v1",
      input: ["text"],
      cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
      contextWindow: 64000,
    },
  ],
  images: {
    "media-images": { generateImages: async (model, context, options) => result },
  },
  classifiers: {
    "media-classifier": { classify: async (model, context, options) => result },
  },
});
```

Model-level `baseUrl` values take precedence over the provider endpoint. If no `models` list is supplied, built-in models of every operation remain registered. Equal model IDs in different operations remain distinct, including their model-specific headers.

Calls made after initial extension loading take effect immediately. Use `pi.unregisterProvider()` to remove the dynamic provider and restore built-in behavior that it replaced.

See the checked [GitLab Duo provider](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/custom-provider-gitlab-duo/) for a complete registration that delegates streaming to built-in API implementations.

## Provide authentication

Static providers can resolve an API key from a literal, environment interpolation, or a command. These values use the same syntax as `models.json`:

- `$NAME` and `${NAME}` read environment variables.
- A leading `!command` uses command output.
- `$$` emits a literal `$`.
- `$!` emits a literal leading `!`.

Use native provider authentication when the integration needs stored credentials, custom resolution, provider-scoped environment, or multiple login methods.

An OAuth provider supplies a display name, login flow, token refresh, and access-token resolution. After registration it appears in `/login`, and Pi stores returned credentials in `~/.pi/agent/auth.json`.

OAuth callbacks are UI-neutral. They can open an authorization URL, show a device code, report progress, request input, or ask the user to choose a login method. Honor cancellation and the supplied abort signal during network requests.

Never write access tokens, refresh tokens, authorization headers, or complete provider responses to ordinary logs.

## Supply and refresh models

Every model needs an ID, display name, input capabilities, and cost metadata. Chat and classifier models also need a context window; chat models need an output limit and reasoning support; image models declare their output modalities. Choose the API implementation at the provider level unless one model requires an override.

Set `promptCache.short` or `promptCache.long` to the provider's best-effort cache lifetime in seconds when Pi should keep an idle prompt cache warm. Leave them unset to disable cache warming for that retention tier.

Compatibility flags describe verified differences in an otherwise supported API. Do not enable them based only on an endpoint claiming compatibility.

Confirm the request fields and response behavior against the actual server.

Use `refreshModels` when the available catalog comes from a live service. Pass `context.signal` to blocking I/O so callers can cancel refreshes.

The two registration forms have different refresh contracts:

- A complete `Provider` returns nothing. It calls `context.publish({ update })` to install provider-owned model state, after which its synchronous `getModels()` exposes the latest list.
- Legacy `ProviderConfig.refreshModels` returns mixed-operation model definitions. Pi replaces that registration’s live models with the returned list and applies any requested persistence.

Publish persisted catalog data only when it should survive across runs. A live service such as llama.cpp can update its in-memory list without persisting it; a remote catalog can retain a snapshot for offline startup.

## Reuse a supported streaming API

Use one of Pi AI’s API implementations whenever the provider protocol matches it.

Supported implementations cover Anthropic Messages, OpenAI Chat Completions and Responses, Google Generative AI and Vertex, Azure OpenAI Responses, Mistral Conversations, and Bedrock Converse.

The provider can still customize authentication, base URLs, headers, model filtering, and discovery while delegating request conversion and streaming to an existing API implementation.

This is safer than copying a stream implementation because it preserves Pi’s message conversion, tool handling, usage accounting, cancellation, and compatibility behavior.

## Implement custom streaming

Implement `streamSimple` only when no existing API implementation can represent the service. Study the implementations under [`packages/ai/src/api`](https://github.com/earendil-works/pi/tree/main/packages/ai/src/api) first.

The stream receives a normalized `TranscriptContext`. System prompts and tool declarations live in transcript system messages, so read them with `getCurrentSystemPrompt(context.messages)` and `getCurrentTools(context.messages)` rather than expecting `context.systemPrompt` or `context.tools`. A model that supports mid-conversation system messages can receive them in place; otherwise call `collapseSystemMessages(context)` to fold later system messages into the leading one.

A custom stream must:

1. Create an assistant message with provider, model, timestamp, pending stop reason, content, and zeroed usage.
2. After request setup succeeds, emit one `start` event before content events.
3. Update the message while emitting balanced text, thinking, and tool-call events.
4. Finalize usage, cost, content, and stop reason.
5. Emit exactly one terminal `done` or `error` event and close the stream.
6. Convert cancellation into an aborted result.

Request setup can fail before `start`; in that case the stream can terminate directly with `error`. Missing request authentication may also throw synchronously before a stream is returned.

Content indexes refer to blocks in the assistant message. Update each block before emitting the event whose `partial` field exposes that state. Tool-call arguments must contain valid parsed input by `toolcall_end`.

The stream must also honor request instrumentation supplied through `SimpleStreamOptions`:

- Call `options.onPayload` before sending the provider request and use any replacement payload it returns.
- Call `options.onResponse` after receiving the response but before consuming its body.
- Await `options.onProviderStreamEvent?.(providerEvent, model)` for each parsed provider event before normalizing it.
- Pass through the abort signal and provider-scoped environment.

These hooks power extension request inspection, response-header events, and provider-stream observation. Omitting them makes the provider behave differently from Pi’s built-in providers.

## Report failures and usage

Set a concrete terminal stop reason. Error and aborted messages need an `errorMessage`; successful messages need accurate input, output, cache, total-token, and cost values.

Pi can compact and retry after recognized context-overflow errors. If the service uses an unknown message, normalize only that provider’s overflow response to `context_length_exceeded` in a guarded `message_end` handler.

Do not rewrite rate limits or transient provider failures as context overflow. Those failures use Pi’s normal retry behavior instead.

## Test the integration

Test at least:

- ordinary and empty text responses
- tool calls and tool results
- image input and image tool results when supported
- usage and cost accounting
- abort behavior
- context overflow
- malformed or partial streams
- Unicode boundaries
- cross-provider session handoff
- authentication refresh and cancellation

The provider tests under [`packages/ai/test`](https://github.com/earendil-works/pi/tree/main/packages/ai/test) define the behavior expected from built-in providers. Adapt the relevant suites rather than relying only on manual prompts.

Run the extension directly while developing, then move it to a discovered extension location or distribute it through a [Pi package](../03-customize-pi/05-packages.md). Use `/reload` after changing a discovered provider extension in an active session.


<!-- ============================================================ -->
<!-- SOURCE: 04-build-on-pi/03-virtual-models.md -->
<!-- ============================================================ -->

# Virtual Models

A virtual model is a selectable model that picks a physical model for each request. Use one to route by task, cost, or conversation state. For example, a router can send quick questions to a small model and hard problems to a large one, while the user selects a single model.

Register virtual models from an [extension](../04-build-on-pi/01-extensions.md). They appear in `/model`, `--model`, scoped models, and settings like any other model. A virtual model can be listed under any provider, including one with physical models, such as `openai-codex/auto`.

## Selection and dispatch

A virtual model selects a model and a thinking level. A router maps that pair to a physical pair for each request:

```
selected (virtual model, virtual level)  ->  dispatched (physical model, physical level)
jev/auto:low                             ->  anthropic/claude-sonnet-4-5:high
```

The virtual thinking level is an input to the router. Its meaning is up to the router; it need not correspond to a reasoning budget.

Pi keeps the two pairs apart:

| | Selection | Dispatch |
|---|---|---|
| Recorded in | `model_change` and `thinking_level_change` entries | Each assistant message: `provider`, `api`, `model`, `thinkingLevel` |
| Visible as | `ctx.model`, `ctx.thinkingLevel`, `PI_MODEL`, `PI_REASONING_LEVEL`, `/model` | The assistant message of each response |

Providers only receive physical models. Assistant messages name the physical model, so replaying a conversation across different physical models works the same as after a manual model switch. Resuming a session restores the virtual selection from its latest `model_change` entry. If the virtual model is no longer registered, Pi falls back to the physical model that answered last.

In interactive mode, the footer shows the routed model next to the selection, for example `auto • high → gpt-5.6-luna • medium`. `/session` lists the cost for each physical model.

Context usage uses the limits of the physical model that produced the latest response, even if that response came before switching to the virtual model. Without such a response, it uses the limits declared on the virtual model, if any. Compaction checks the same limits, and again the limits of the model each request is routed to. If that model's context window is too small for the conversation, Pi compacts before sending the request; the route stays as the router chose it.

## Register a virtual model

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerVirtualModel({
    provider: "router",
    id: "auto",
    name: "Auto",
    thinkingLevels: ["low", "high"],
    route(request, ctx) {
      // Tool follow-ups and retries stay on the model that handled the turn.
      const sticky = request.failed ?? request.previous;
      if (request.reason !== "user" && sticky) {
        return { model: sticky.model, thinkingLevel: sticky.thinkingLevel ?? "medium" };
      }
      const id = request.thinkingLevel === "high" ? "claude-sonnet-4-5" : "claude-haiku-4-5";
      return { model: ctx.modelRegistry.find("anthropic", id)!, thinkingLevel: "medium" };
    },
  });
}
```

- `provider` is the provider the model is listed under. It can be any provider ID. A provider can list several virtual models next to its physical ones. On a physical provider, the virtual model is available when that provider has credentials. Under an ID that no provider uses, it is always available.
- `id` must not be the ID of a physical model of that provider. If a catalog refresh later adds a physical model with the same ID, the virtual model hides it.
- `thinkingLevels` lists the levels offered for selection. It defaults to `["off"]`.
- `contextWindow` and `maxTokens` are shown before the first response. Unset limits are unknown.
- `input` lists the input types offered for selection. It defaults to text and images; physical models without image support receive placeholders.

Registration follows the same queuing and reload rules as `pi.registerProvider()`. Registering the same provider and ID again replaces the virtual model. `pi.unregisterVirtualModel(provider, id)` removes it; `pi.unregisterProvider()` does not. SDK code can register one without an extension: `modelRuntime.registerVirtualModel(definition)`.

## Route requests

`route(request, ctx)` runs before every request made with the virtual model and returns `{ model, thinkingLevel }`. The model can be any physical model in the catalog whose provider has credentials; look it up with `ctx.modelRegistry`. A virtual model cannot route to another virtual model. Pi clamps the thinking level to the returned model.

| Field | Meaning |
|---|---|
| `model`, `thinkingLevel` | The selected virtual model and level |
| `reason` | Why the request is made, see below |
| `previous` | Physical model and thinking level of the latest successful response in `messages` |
| `failed` | For `retry`: physical model, thinking level, and assistant `message` of the failed request, which `messages` no longer contains. The message carries `stopReason` and `errorMessage`. Absent when routing itself failed |
| `state` | Router state last returned on this session branch, see below |
| `messages` | The conversation for this request, including system messages |
| `signal` | Abort signal of the request |

| `reason` | Request |
|---|---|
| `user` | First request after a message the user wrote, including steering and follow-up messages |
| `continuation` | Any other request in the agent loop, such as after tool results or extension messages |
| `retry` | Automatic retry after a failed request, including after compaction for a context overflow |
| `direct` | Request made outside the agent loop, such as a compaction summary or an extension calling `ctx.modelRegistry.streamSimple()` |

Returning `previous` for `continuation` and `failed` for `retry` keeps prompt caches and thinking signatures valid. Switching models between turns is allowed but loses the prompt cache. A retry can also switch to another model, for example when `failed.message.errorMessage` reports that a provider is overloaded or the context overflowed.

If `route()` throws, or returns a virtual model or a model without credentials, the request ends with an error response.

## Keep routing state

`route()` can return `state` next to the model. Pi stores it on the session branch and passes it back as `request.state` on later requests. Use it for decisions the transcript does not record, such as classifier results or a routing phase:

```typescript
pi.registerVirtualModel<{ phase: "plan" | "build" }>({
  provider: "router",
  id: "phased",
  name: "Phased",
  route(request, ctx) {
    const state = request.state ?? { phase: "plan" };
    const id = state.phase === "plan" ? "claude-opus-4-5" : "claude-haiku-4-5";
    return { model: ctx.modelRegistry.find("anthropic", id)!, thinkingLevel: "medium", state };
  },
});
```

- State must be JSON-serializable. Returning `undefined` or `request.state` itself keeps the current state.
- Pi stores any other returned object as new state, before the request is sent, even when it equals the current state. Return a new object only when the state changes. The state stays stored if the request later fails.
- State follows the session tree, so forks and `/tree` navigation see the state of their branch. It survives compaction.
- `direct` requests have no state, and Pi ignores state they return.

The transcript already records the selection and every dispatched model, and `ctx.sessionManager.getBranch()` exposes both.

Routers can call other models through `ctx.modelRegistry`, for example `ctx.modelRegistry.classify()` with a classifier model from `ctx.modelRegistry.findOfType("classifier", provider, id)`. The call adds latency before the first token of the turn.

See [`jev-router.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/jev-router.ts) for a complete router. It plans on a strong OpenAI Codex model chosen by the Jev classifier, lets that model make the first edit, and then switches once to a cheaper model, accepting a single prompt-cache miss. It keeps the phase as router state.


<!-- ============================================================ -->
<!-- SOURCE: 04-build-on-pi/04-tui.md -->
<!-- ============================================================ -->

# Terminal UI

`@earendil-works/pi-tui` provides the terminal component system used by Pi. Extensions use it when built-in dialogs, notifications, status text, and widgets are not enough for the interaction they need.

Start with `ctx.ui` methods from an [extension](../04-build-on-pi/01-extensions.md#interact-with-the-user). Build a custom component only when the UI needs its own rendering, keyboard or mouse input, focus, layout, or lifecycle.

## Choose an integration point

| Need | Use |
|---|---|
| Select, confirm, input, or multi-line editor | `ctx.ui.select()`, `confirm()`, `input()`, or `editor()` |
| Non-blocking feedback | `ctx.ui.notify()` or `setStatus()` |
| Persistent content near the editor | `ctx.ui.setWidget()` |
| Replace the header, footer, or editor | The corresponding `ctx.ui` component factory |
| Temporary interactive screen or overlay | `ctx.ui.custom()` |
| Custom rendering for a tool or session entry | An extension renderer |

These APIs receive Pi’s active theme and keybindings where needed. Do not create a second terminal renderer inside an extension.

## Understand the component model

A component renders an array of terminal lines for an available width. It can optionally handle keyboard and mouse input, and it must invalidate cached output when its state or theme-dependent content changes.

Every rendered line must fit within the supplied width. Measure visible terminal columns rather than string length because ANSI escapes, wide characters, emoji, and combining characters change display width.

Use `visibleWidth()`, `truncateToWidth()`, `sliceByColumn()`, and `wrapTextWithAnsi()` instead of implementing terminal-width handling yourself. Pi resets styling and hyperlinks after every line, so reapply styles on each rendered line.

After changing component state, invalidate the affected component and call the injected `tui.requestRender()`. The TUI coalesces render requests and updates the terminal.

## Compose built-in components

The package includes components for common layouts and controls:

- `Text`, `Markdown`, `Image`, and `TruncatedText` render content.
- `Container`, `VStack`, `HStack`, `Box`, and `Spacer` compose layouts.
- `Input` and `Editor` accept text.
- `SelectList` and `SettingsList` implement searchable selection and settings flows.
- `ScrollView` provides a bounded scrollable viewport.
- `Loader` and `CancellableLoader` report ongoing work.
- `MouseRegion` adds pointer behavior around another component.

Prefer these components over rebuilding selection, scrolling, text editing, or width handling. The extension examples show how to combine them with Pi’s borders and themes.

## Handle keyboard input and focus

Use `matchesKey()` and `Key` for terminal keyboard input. The parser accounts for supported terminal protocols and key modifiers. Extension components should use the injected `KeybindingsManager` for configurable application actions.

A component that displays a text cursor should implement `Focusable` and place `CURSOR_MARKER` immediately before its visual cursor. The TUI uses that marker to position the hardware cursor for input method editors.

Containers that wrap an `Input` or `Editor` must propagate their `focused` state to that child. Without propagation, Chinese, Japanese, Korean, and other IME candidate windows can appear at the wrong screen position.

Extend Pi’s `CustomEditor` when replacing the main editor. It preserves application shortcuts and agent controls.

Forward keys your editor does not own to the base implementation, and restore the default by clearing the custom editor factory.

## Handle mouse input

Fullscreen mode routes normalized mouse events to components. A handler can mark an event handled, capture a drag sequence, request focus, or request a render.

Unhandled wheel events scroll the nearest `ScrollView`. Unhandled primary-button drags remain available for transcript selection. OSC 8 links take precedence over enclosing click regions.

Regular mode leaves mouse input to the terminal because the terminal owns scrollback. Design every interaction with a keyboard path even when fullscreen mouse input is available.

## Use custom screens and overlays

`ctx.ui.custom()` temporarily gives one component control of the interactive area and resolves when that component calls the supplied completion callback.

Pass `overlay: true` to draw above existing content. Overlay options control size, anchors, offsets, margins, and responsive visibility. An overlay handle can change focus or temporarily hide and show the overlay with `setHidden()` while the interaction remains active.

Focused overlays retain input ownership across ordinary renders. If another component should receive input while an overlay remains visible, explicitly release or redirect focus through the handle.

Treat each custom component instance as belonging to one interaction. Create a new instance when starting that interaction again.

Finish the interaction with the completion callback supplied to the component factory. It resolves the `ctx.ui.custom()` promise and disposes the component. Do not call `OverlayHandle.hide()` on an overlay created by `ctx.ui.custom()`.

See [`overlay-qa-tests.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/overlay-qa-tests.ts) for positioning, stacking, focus, responsive visibility, and animation behavior.

## Apply themes correctly

Use the theme passed to the extension or component callback. Theme helpers produce ANSI-styled strings for semantic colors such as accent, muted text, success, warnings, errors, tool output, and Markdown.

Use `theme.style()` to combine foreground and background colors with text attributes:

```typescript
return new Text(
  theme.style("Done!", {
    fg: "success",
    bg: "toolSuccessBg",
    bold: true,
  }),
  0,
  0,
);
```

A style color can be a semantic theme token or a concrete `Color`. Foreground tokens are accepted as `fg` and background tokens as `bg`; to use a token's color in the other position, pass its concrete color, for example `{ fg: theme.colors.userMessageBg }`. Access concrete colors through `theme.colors` and use utilities such as `mixColors()` from `@earendil-works/pi-tui` when color math is needed. Tokens that a theme sets to the terminal default render with the terminal's own color; `theme.colors` reports the color the terminal announced for them, or a guess when it did not. Use `theme.appearance` (`"dark"` or `"light"`) to decide, for example, whether to lighten or darken a color. Pi converts the result to truecolor or 256-color output based on terminal capabilities. Theme tokens are converted once per theme; compute concrete colors outside the render path when possible.

The existing `theme.fg()` and `theme.bg()` helpers remain available for applying one semantic color.

Do not permanently store strings with theme colors unless `invalidate()` rebuilds them. A theme change clears render caches, but it cannot remove old ANSI colors embedded in application state.

Theme callbacks evaluated during rendering do not need special rebuilding. Stateless components can also calculate themed output on every render.

Use [Themes](../03-customize-pi/04-themes.md) to create terminal palettes. Use Pi’s `getMarkdownTheme()` when rendering Markdown that should match the active application theme.

## Keep rendering responsive

Rendering runs on the interactive path. Cache expensive layout and highlighting work by width and content, then clear that cache from `invalidate()`.

Keep the default view compact and reveal detail through expansion or a dedicated screen. For custom tool rendering, handle partial results and reuse the previous component when it can be updated safely.

Use `PI_TUI_WRITE_LOG` to capture the raw ANSI stream when diagnosing rendering problems. Test narrow widths, wide characters, resize events, theme changes, focus transitions, and both regular and fullscreen modes.

## Examples and source

The checked extension examples cover the main patterns:

- [`preset.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/preset.ts) and [`tools.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/tools.ts) use selection and settings lists.
- [`qna.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/qna.ts) uses cancellable asynchronous UI.
- [`modal-editor.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/modal-editor.ts) replaces the editor.
- [`custom-footer.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/custom-footer.ts) replaces the footer.
- [`widget-placement.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/widget-placement.ts) places persistent content around the editor.
- [`doom-overlay/`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/doom-overlay/) demonstrates a continuously rendered overlay.

The public exports are defined in [`packages/tui/src/index.ts`](https://github.com/earendil-works/pi/blob/main/packages/tui/src/index.ts). See [Extensions](../04-build-on-pi/01-extensions.md) for extension lifecycle, state, tools, events, and mode behavior.


<!-- ============================================================ -->
<!-- SOURCE: 04-build-on-pi/05-cli-integration.md -->
<!-- ============================================================ -->

# CLI Integration

By default, running `pi` opens the interactive terminal interface. When input or output is piped or redirected, Pi uses print mode instead. You can also select print, JSON, or RPC mode explicitly for scripts and applications.

All four modes use the same agent, sessions, resources, and tools. The mode determines how input enters Pi, how output is exposed, and whether the process remains available for more commands.

The SDK is not a CLI mode. It embeds the agent directly in a Node.js or Bun process. See the [SDK](../04-build-on-pi/06-sdk.md) when direct TypeScript access is preferable to a process boundary.

## Choose a mode

| Mode | Interface | Lifetime | Use it when |
|---|---|---|---|
| Interactive | Terminal UI | Until the user exits | A person is working with Pi directly |
| Print | Final text on stdout | One invocation | A script needs the final assistant response |
| JSON | JSONL events on stdout | One invocation | A process needs structured progress from a run |
| RPC | JSONL commands, responses, and events | Long-lived | A process needs bidirectional control |

CLI options still select the working directory, model, tools, resources, and session persistence independently of the mode. See [Command Line](../05-reference/01-cli.md) for the complete startup options.

## Print to stdout

Print mode runs the supplied prompts, writes the final assistant text to stdout, and exits:

```bash
pi --print "Summarize the changes in this repository"
```

Use print mode when only the final text is needed, including command substitution, pipelines, and one-shot jobs. Intermediate events are not exposed.

Print mode writes errors to stderr. A final assistant response with an `error` or `aborted` stop reason produces a nonzero exit status.

When no mode is selected explicitly, non-TTY stdin or stdout also selects print mode. This allows piped input and output without adding `--print`.

## Stream JSON events

JSON mode writes a session header followed by agent and session events as newline-delimited JSON:

```bash
pi --mode json "Review this repository" > events.jsonl
```

This is structured event output, not a single JSON result or a constraint on the format of the model’s response.

All prompts are supplied when the process starts. The process streams events for that run and then exits; it does not accept later commands.

A failed or aborted assistant response appears in the event stream but does not by itself produce a nonzero exit status. Inspect the events when success or failure matters. Pi still exits nonzero if the invocation throws an error.

Streaming `message_update` records contain deltas rather than a growing message snapshot. Assemble live output from the delta events, then replace it with the authoritative message from `message_end`.

`agent_end` can be followed by automatic recovery or queued work. `agent_settled` marks the end of automatic work for the current run.

Stdout is reserved for JSONL. Diagnostics and application logging are written to stderr. See [JSON Event Stream](../05-reference/10-json.md) for framing, event shapes, and reconstruction rules.

## Control Pi with RPC

RPC mode keeps Pi running while another process sends commands and receives responses and events:

```bash
pi --mode rpc --no-session
```

Commands are JSON objects written to stdin. Responses and events are JSON objects written to stdout. Every record occupies one line.

Add an `id` to commands that need correlation. The matching response repeats that ID. Events generally have no command ID because they describe session activity rather than one request.

A successful `prompt` response means the prompt was accepted, queued, or handled. It does not mean the run completed. Continue consuming events through `agent_settled` when completion matters.

RPC commands can change models, inspect state, manage sessions, run shell commands, and answer extension UI requests.

Extension dialogs form a request-response subprotocol. Other extension UI updates are notifications that a client may display or ignore. TUI-only extension capabilities are unavailable or degraded outside interactive mode.

For Node.js or TypeScript integrations, prefer `RpcClient` from `@earendil-works/pi-coding-agent`. It starts a Pi RPC child process, correlates requests, exposes typed command methods, and delivers session events to listeners.

The [RPC client example](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/rpc-client.ts) sends one prompt, streams text and tool activity, waits for `agent_settled`, and shuts down the child process. It is included in the repository’s TypeScript checks.

`RpcClient.promptAndWait()` installs its event listener before sending the prompt, avoiding a race with fast completions. For separate operations, subscribe before calling `prompt()` and call `waitForIdle()` only while a run is active.

The client requires a path to a runnable Pi CLI. The repository example points at `dist/cli.js`, so the package must be built before that example runs from a checkout.

If you are building a client without `RpcClient`, start with [RPC Protocol](../05-reference/11-rpc.md), then use [RPC Commands](../05-reference/12-rpc-commands.md) and [JSON Event Stream](../05-reference/10-json.md) as the wire references.

## Fork and rebrand Pi

A source fork can change the CLI name and configuration directory through `package.json`:

```json
{
  "piConfig": {
    "name": "my-agent",
    "configDir": ".my-agent"
  }
}
```

Change the top-level `bin` field to set the executable name. These settings affect the CLI banner, configuration paths, and derived environment variable names.

## Examples and references

- [RPC client](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/rpc-client.ts): typed Node.js integration
- [RPC extension UI](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/rpc-extension-ui.ts): custom terminal client with extension dialogs
- [Command Line](../05-reference/01-cli.md): startup options and mode selection
- [JSON Event Stream](../05-reference/10-json.md): JSON event reference
- [RPC Protocol](../05-reference/11-rpc.md): RPC lifecycle, framing, errors, and shutdown
- [RPC Commands](../05-reference/12-rpc-commands.md): command and response reference
- [RPC Extension UI](../05-reference/13-rpc-extension-ui.md): extension interaction subprotocol
- [SDK examples](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/): in-process TypeScript integrations


<!-- ============================================================ -->
<!-- SOURCE: 04-build-on-pi/06-sdk.md -->
<!-- ============================================================ -->

# SDK

`@earendil-works/pi-coding-agent` embeds Pi in a Node.js or Bun process. It provides direct TypeScript access to the agent, sessions, tools, models, and resources used by the command-line application.

Use the SDK for in-process TypeScript integration. For a language-independent or isolated subprocess, see [CLI Integration](../04-build-on-pi/05-cli-integration.md).

```typescript
import { createAgentSession } from "@earendil-works/pi-coding-agent";

const { session } = await createAgentSession();

try {
  await session.prompt("What files are in the current directory?");
  console.log(session.getLastAssistantText());
} finally {
  session.dispose();
}
```

This uses the working directory, discovered resources, stored settings, and configured credentials. `prompt()` resolves when the run finishes.

The [complete minimal example](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/01-minimal.ts) also streams text events. All [SDK examples](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/) are typechecked with the repository.

<a id="session-management"></a>

## Session lifecycle

`createAgentSession()` creates an `AgentSession`. The session owns one conversation, its model and tools, queued messages, compaction state, and extension runtime.

Read current state through `session.messages`, `session.model`, `session.thinkingLevel`, `session.systemPrompt`, and `session.getActiveToolNames()`.

`session.systemPrompt` is read-only and returns the current effective system prompt, including changes that have not yet been sent to the model. Tool changes are declared to the model before the next request.

<a id="sessionmanager-api"></a>

### Session storage

Sessions are persistent by default. `SessionManager` owns the persisted or in-memory entry tree and tracks its active leaf. Branching changes that leaf without deleting abandoned branches. When Pi reconstructs model context, the manager selects the active branch and applies compaction.

`SessionManager` is authoritative for finalized model context. Restore external history by constructing the session with a manager containing those entries. Assigning `session.agent.state.messages` does not replace persisted context.

Use an in-memory manager when the host does not want session files:

```typescript
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";

const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
});
```

See the checked [sessions example](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/11-sessions.ts) for creating, opening, continuing, listing, and forking sessions. [Session File Format](../05-reference/08-session-format.md) defines the persisted JSONL contract, and [Message Types](../05-reference/14-message-types.md) defines transcript values. For exact methods and signatures, use the exported TypeScript declarations or [`session-manager.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/session-manager.ts).

`cwd` selects the workspace used for project resource discovery, context files, session grouping, and built-in tool paths. Pass it explicitly when the target differs from `process.cwd()`.

`session.dispose()` aborts active work, invalidates extension contexts, disconnects from the agent, and removes event listeners. Call it when the session is no longer needed.

`AgentSessionRuntime` adds `newSession()`, `switchSession()`, `fork()`, and `importFromJsonl()`. Each operation replaces the active `AgentSession` and recreates services for the target working directory.

After a runtime replacement, subscriptions belong to the old `AgentSession` and must be rebound. See the [session runtime example](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/13-session-runtime.ts).

## Prompting

`prompt()` handles extension commands and expands file-based prompt templates before ordinary user messages enter the agent. For an accepted agent run, it resolves after the run finishes, including automatic retries.

A prompt sent while the session is already streaming must specify whether it should steer the current run or follow it. Calling `prompt()` without that choice rejects rather than guessing.

A steering message enters after the current assistant turn and its tool calls. A follow-up enters after the current run finishes its pending work. `steer()` and `followUp()` expose those behaviors directly and return `"queued"` if the input was queued (including after an extension transformed it), or `"handled"` if an extension consumed it.

`abort()` stops the active operation and waits for the session to become idle. `waitForIdle()` waits without aborting it.

## Subscribing to events

Subscribe before prompting when the host needs streamed output:

```typescript
const unsubscribe = session.subscribe((event) => {
  if (event.type === "message_update" && event.assistantMessageEvent.type === "text_delta") {
    process.stdout.write(event.assistantMessageEvent.delta);
  }
});

try {
  await session.prompt("Explain this repository");
} finally {
  unsubscribe();
}
```

Session events report message updates, tool execution, queues, compaction, retries, and run lifecycle changes.

`message_end` contains the authoritative completed message. `agent_end` marks the end of one low-level agent run, but automatic recovery or queued work can still follow.

Use `agent_settled` when the host needs to know that Pi will not continue automatically.

## Configuring a session

Without overrides, the factory creates a `ModelRuntime`, file-backed `SettingsManager`, persistent `SessionManager`, `DefaultResourceLoader`, and the configured default tools.

Each boundary can be supplied explicitly:

- `modelRuntime`, `model`, `thinkingLevel`, and `scopedModels` control model access and selection.
- `settingsManager` supplies merged settings or an in-memory configuration.
- `sessionManager` supplies persistent or in-memory conversation history.
- `resourceLoader` supplies extensions, skills, prompt templates, themes, and context files.
- `tools`, `noTools`, `excludeTools`, and `customTools` control the active tool set.

Use `DefaultResourceLoader` when you want standard discovery with selected overrides. Supply a custom `ResourceLoader` when the host owns resource storage and discovery completely.

<a id="inlineextension"></a>

Inline extension factories can be supplied through `DefaultResourceLoader`. Give one an `InlineExtension` name only when it needs a stable name in diagnostics and startup output. A named inline extension with `replaceable: true` is left out when another extension registers a tool, command, or flag with a name it registers during loading, instead of both loading with a conflict. The CLI's built-in codemode, tool search, and MCP extensions are replaceable. A named entry with `builtin: true` is not an inline extension: it supplies the code of the `builtin:<name>` extension, which loads like a configured extension file. It loads by default, is listed in `pi config`, and is disabled by `-builtin:<name>` in the `extensions` setting or by `noExtensions`; `additionalExtensionPaths: ["builtin:<name>"]` loads it explicitly. It loads after project trust is resolved, so it cannot handle `project_trust`. The CLI's built-in extensions use it.

<a id="codemode-mcp"></a>

The CLI loads `codemode`, `tool_search`, and MCP as built-in extensions. SDK sessions do not; add `createCodemodeExtension()`, `createToolSearchExtension()`, and `createMcpExtension()` to the `extensionFactories` of `DefaultResourceLoader`. `codemode` and `tool_search` are registered inactive: enable them through the `defaultTools` setting (`["+codemode", "+tool_search"]` keeps the other default tools), or let the MCP extension activate them: `codemode` for servers with `codemode` exposure, `tool_search` for servers with `deferred` exposure. The MCP extension connects its servers on `session_start`, so call `session.bindExtensions()`. See [Codemode and MCP](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/14-codemode-mcp.ts).

See the focused examples for [models](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/02-custom-model.ts), [tools](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/05-tools.ts), [extensions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/06-extensions.ts), and [full control](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/12-full-control.ts).

## Examples

| Example | Purpose |
|---|---|
| [Minimal](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/01-minimal.ts) | Create, prompt, observe, and dispose a session |
| [Custom model](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/02-custom-model.ts) | Select a model and thinking level |
| [System prompt](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/03-custom-prompt.ts) | Replace or append to the system prompt |
| [Skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/04-skills.ts) | Discover, filter, and add skills |
| [Tools](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/05-tools.ts) | Select built-in tools and their working directory |
| [Extensions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/06-extensions.ts) | Load file-based and inline extensions |
| [Context files](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/07-context-files.ts) | Add or replace project instructions |
| [Prompt templates](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/08-prompt-templates.ts) | Add file-style prompt templates |
| [Credentials](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/09-api-keys-and-oauth.ts) | Configure credential and model storage |
| [Settings](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/10-settings.ts) | Supply file-backed or in-memory settings |
| [Sessions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/11-sessions.ts) | Control session persistence and restoration |
| [Full control](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/12-full-control.ts) | Replace default discovery and state services |
| [Session runtime](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/13-session-runtime.ts) | Replace the active session safely |
| [Codemode and MCP](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/sdk/14-codemode-mcp.ts) | Add the `codemode`, `tool_search`, and MCP extensions |

<a id="exports"></a>

## Resources

- [Choose a Model](../02-run-pi/02-models.md) covers model selection and compatible endpoints; [Providers](../05-reference/07-providers.md) covers credentials and provider-specific setup.
- [Configuration](../03-customize-pi/01-configuration.md) explains normal discovery and settings; [Settings](../05-reference/04-settings.md) lists every setting.
- [Sessions and Context](../02-run-pi/03-sessions.md) explains session behavior; [Session Format](../05-reference/08-session-format.md) defines persisted entries; [Message Types](../05-reference/14-message-types.md) defines shared transcript values.
- [Extensions](../04-build-on-pi/01-extensions.md), [Skills](../03-customize-pi/03-skills.md), and [Prompt Templates](../03-customize-pi/02-prompt-templates.md) document resources supplied through a `ResourceLoader`.
- [CLI Integration](../04-build-on-pi/05-cli-integration.md) covers print, JSON, and RPC alternatives to an in-process SDK integration.


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/01-cli.md -->
<!-- ============================================================ -->

<a id="cli-and-modes-reference"></a>

# Command Line

This page documents Pi's built-in command-line commands and options. Run `pi --help` or append `--help` to a command for the exact interface in your installed version. The top-level help also includes options registered by loaded extensions.

```sh
pi [options] [--] [@files...] [messages...]
pi install <source> [options]
pi remove <source> [options]
pi uninstall <source> [options]
pi update [target] [options]
pi list
pi config [options]
pi auth <check|print-api-key|print-bearer-token> [options]
pi mcp <list|login|logout> [options]
```

<a id="modes"></a>

## Invocation and output

```sh
pi
pi --print "Summarize this repository"
git diff | pi --print "Review this change"
pi --mode json "Inspect this repository" > events.jsonl
```

With terminal stdin and stdout, Pi opens the terminal UI unless `--print`, `--mode json`, or `--mode rpc` selects another interface. When either stream is redirected and neither JSON nor RPC mode is selected, Pi uses print mode. See [CLI Integration](../04-build-on-pi/05-cli-integration.md) for choosing between interactive, print, JSON, RPC, and SDK integration.

| Input | Behavior |
|---|---|
| `message` | Provide an initial prompt |
| `@path` | Include a text file or image in the first prompt |
| Piped stdin | Prepend its contents to the first prompt |
| `--` | Stop option parsing so a prompt can begin with `-` |

Pi resolves `@path` from the current working directory. The working directory also controls project configuration, resource discovery, and session grouping.

`--print` controls whether Pi runs once and exits. `--mode` selects the output interface. `--mode text` does not force one-shot execution when stdin and stdout are terminals; use `--print` for that behavior.

| Option | Behavior |
|---|---|
| `-p`, `--print` | Run the supplied prompts, write the final assistant text to stdout, then exit |
| `--mode text` | Select text output; still open the terminal UI when stdin and stdout are terminals |
| `--mode json` | Run the supplied prompts, write JSONL events to stdout, then exit |
| `--mode rpc` | Read JSONL commands from stdin and write responses and events to stdout until shutdown |
| `--export <input> [output]` | Export a session file to HTML and exit; derive the destination when `output` is omitted |

RPC mode rejects `@file` arguments. JSON and RPC modes reserve stdout for protocol records. See [JSON Event Stream](../05-reference/10-json.md) and [RPC Protocol](../05-reference/11-rpc.md).

<a id="model-options"></a>

## Models

```sh
pi --model sonnet:high
```

See [Choose a Model](../02-run-pi/02-models.md) for model selection and [Providers](../05-reference/07-providers.md) for credentials.

- `--provider <name>`<br>
  Restricts `--model` lookup to one provider. It requires `--model`.
- `--model <pattern>`<br>
  Selects by exact ID or fuzzy ID/name match. It accepts `provider/id` and an optional `:<thinking>` suffix.
- `--api-key <key>`<br>
  Uses a non-persistent API-key override. It requires a model selected through `--model` or `--models`.
- `--thinking <level>`<br>
  Sets `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, or `max`. It overrides a `--model` suffix and is clamped to the model's capabilities.
- `--models <patterns>`<br>
  Sets a comma-separated scope for startup and cycling. It accepts exact IDs, fuzzy matches, case-insensitive globs, and optional `:<thinking>` suffixes.
- `--list-models [search]`<br>
  Lists available models, optionally filtered by a fuzzy search, then exits.

<a id="session-options"></a>

## Sessions

```sh
pi --continue
```

See [Sessions and Context](../02-run-pi/03-sessions.md) for resuming, forking, naming, and storing sessions.

- `-c`, `--continue`<br>
  Continues the most recent session for the current project.
- `-r`, `--resume`<br>
  Opens the session selector.
- `--session <path|id>`<br>
  Opens by file path, exact ID, or partial ID. Pi searches the current project first and offers to fork a cross-project match.
- `--session-id <id>`<br>
  Opens the exact project session ID or creates it if absent. IDs accept letters, numbers, `.`, `_`, and `-`.
- `--fork <path|id>`<br>
  Forks an existing session into a new session for the current project.
- `--session-dir <dir>`<br>
  Overrides storage and lookup. It takes precedence over `PI_CODING_AGENT_SESSION_DIR` and the `sessionDir` setting.
- `--no-session`<br>
  Uses an in-memory session that is not persisted.
- `-n`, `--name <name>`<br>
  Sets the session display name.

Constraints:

- Session IDs must start and end with a letter or number.
- `--fork` cannot be combined with `--session`, `--continue`, `--resume`, or `--no-session`.
- `--session-id` cannot be combined with `--session`, `--continue`, or `--resume`. Combine it with `--fork` to choose the new ID.

<a id="tool-options"></a>

## Tools

```sh
pi --tools read,grep,find,ls --print "Review this project"
```

See [Settings](../05-reference/04-settings.md#tools) for configuring the default tool selection.

- `-t`, `--tools <list>`<br>
  Replaces the default selection with a comma-separated allowlist of built-in, extension, or custom tools.
- `-xt`, `--exclude-tools <list>`<br>
  Disables comma-separated tool names after all other selection options.
- `-nbt`, `--no-builtin-tools`<br>
  Disables default built-in tools while retaining extension and custom tools.
- `-nt`, `--no-tools`<br>
  Starts with all built-in, extension, and custom tools disabled.

Default enabled tools are `read`, `bash`, `edit`, and `write`, unless `defaultTools` changes them. `--tools` replaces the whole selection, so name every tool you want; `defaultTools` also accepts `+name` and `-name` to change the defaults instead.

| Built-in | Purpose |
|---|---|
| `read` | Read text files and supported images |
| `bash` | Run shell commands |
| `powershell` | Run PowerShell commands on Windows |
| `edit` | Apply exact text replacements to an existing file |
| `write` | Create or overwrite a file |
| `grep` | Search file contents |
| `find` | Find paths using glob patterns |
| `ls` | List directory contents |

Built-in extensions add two more tools. They are off by default; the MCP extension turns them on when an MCP server needs them (see [MCP](../03-customize-pi/06-mcp.md#exposure)). To enable them yourself, name them in `--tools` or `defaultTools`.

| Built-in extension | Purpose |
|---|---|
| `codemode` | Run JavaScript that calls the other tools, for example in parallel with `Promise.allSettled`; only the script's output reaches the model |
| `tool_search` | Search tools that are not declared to the model (`codemode` and `deferred` exposure, such as MCP tools) and declare the matches for the next call |

### Enable codemode

To turn on `codemode` for every session, add it to the default tools in `~/.pi/agent/settings.json` or a project's `.pi/settings.json`:

```json
{
  "defaultTools": ["+codemode"]
}
```

This keeps `read`, `bash`, `edit`, and `write` and adds `codemode`. For one invocation, list every tool, since `--tools` replaces the selection:

```sh
pi --tools read,bash,edit,write,codemode
```

Codemode is useful without MCP: scripts can run several tool calls in parallel, filter large output before it reaches the model, call classifier models such as TypeSafe's Jev through `models.classify()` (see [Classifier models](../02-run-pi/02-models.md#use-classifier-models)), and generate images through `models.generateImages()` (see [Image models](../02-run-pi/02-models.md#use-image-models)).

### How codemode works

Scripts run in a QuickJS sandbox and reach the other tools through `tools.<name>(args)`. [Codemode](../05-reference/02-codemode.md) describes the script API, how tools are listed and found, the `store()` and `models` globals, and the limits.

### Tool search

`tool_search` is off by default; enable it with `"defaultTools": ["+tool_search"]` or `--tools`. It uses the same ranking as `searchTools()` over tools that are not declared yet and declares the matches for the next model call. Loaded tools are recorded in the session like other tool changes, so they stay declared on that branch.

<a id="resource-options"></a>

## Resources

```sh
pi --extension ./review.ts
```

See [Configuration](../03-customize-pi/01-configuration.md) for conventional directories and project trust, [Settings](../05-reference/04-settings.md#resources) for configured paths, and [Pi Packages](../03-customize-pi/05-packages.md) for package sources.

- `-e`, `--extension <path>`<br>
  Loads an extension file or directory, or a built-in extension such as `builtin:mcp`, and is repeatable.
- `-ne`, `--no-extensions`<br>
  Disables discovered, configured, and built-in extensions. Explicit `-e` paths still load, so `pi -ne -e builtin:mcp` keeps only the built-in MCP support.
- `--skill <path>`<br>
  Loads a skill file or directory and is repeatable.
- `-ns`, `--no-skills`<br>
  Disables discovered and configured skills. Explicit `--skill` paths still load.
- `--prompt-template <path>`<br>
  Loads a prompt-template file or directory and is repeatable.
- `-np`, `--no-prompt-templates`<br>
  Disables discovered and configured templates. Explicit `--prompt-template` paths still load.
- `--theme <path>`<br>
  Loads a theme file or directory and is repeatable.
- `--use-theme <name[/name]>`<br>
  Selects the initial interactive theme for this run.
- `--no-themes`<br>
  Disables discovered and configured themes. Explicit `--theme` paths still load.
- `-nc`, `--no-context-files`<br>
  Disables `AGENTS.md` and `CLAUDE.md` discovery.

Resource paths apply only to the current process. Relative paths resolve from the current working directory.

<a id="prompt-and-display-options"></a>

## Prompts and process

```sh
pi --append-system-prompt ./instructions.md
```

See [Configuration](../03-customize-pi/01-configuration.md) for saved configuration, [Security](../02-run-pi/04-security.md#understand-project-trust) for project trust, and [Environment Variables](../05-reference/05-environment-variables.md) for process controls.

- `--system-prompt <text|path>`<br>
  Replaces the default system prompt with text or the contents of an existing file.
- `--append-system-prompt <text|path>`<br>
  Appends text or an existing file to the system prompt and is repeatable.
- `--tui-mode <mode>`<br>
  Uses `fullscreen` (default) or `regular` terminal mode.
- `--verbose`<br>
  Shows verbose interactive startup information, overriding `quietStartup`.
- `-a`, `--approve`<br>
  Trusts project-local configuration and resources for this process.
- `-na`, `--no-approve`<br>
  Ignores trust-gated project-local configuration and resources for this process.
- `--offline`<br>
  Disables automatic network activity, including model catalog refreshes. Equivalent to `PI_OFFLINE=1`.
- `-h`, `--help`<br>
  Shows help, including flags registered by loaded extensions, then exits.
- `-v`, `--version`<br>
  Shows the Pi version, then exits.

Extensions may register additional long-form options. Unknown short options are rejected.

## Package commands

```sh
pi install npm:@scope/package
```

See [Pi Packages](../03-customize-pi/05-packages.md) for source formats, filtering, installation, and project scope.

### Common tasks

| Task | Command |
|---|---|
| Install a package | `pi install <source>` |
| List configured packages | `pi list` |
| Remove a package and its settings entry | `pi remove <source>` |
| Configure which package resources load | `pi config` |

Add `--local` or `-l` to `install`, `remove`, `uninstall`, or `config` to use project settings instead of global settings.

### Update Pi or packages

Running `pi update` without a target updates Pi itself.

| Task | Command |
|---|---|
| Update Pi | `pi update` |
| Update all installed packages | `pi update --extensions` |
| Update one installed package | `pi update <source>` |
| Refresh model catalogs | `pi update --models` |
| Update Pi and all installed packages | `pi update --all` |

Add `--force` to reinstall Pi when the selected update includes Pi.

`pi update` cannot update Pi when another package manager provides it, such as Nix. Update Pi with that package manager, for example `nix profile upgrade pi`. Package and model catalog updates still work.

### Aliases and command options

- `pi uninstall <source>` is an alias for `pi remove <source>`.
- `pi update --self`, `pi update self`, and `pi update pi` are aliases for `pi update`.
- `pi update --extension <source>` is an alias for `pi update <source>`.
- `-a`, `--approve` trusts project-local files for one command. `-na`, `--no-approve` ignores trust-gated project-local files.
- Append `-h` or `--help` to a command for its exact usage and option constraints.

## Credential commands

```sh
pi auth check --provider openai --json
```

Authentication commands require `--provider <provider>` or `--model <model>`. See [Providers](../05-reference/07-providers.md) for supported methods.

| Command | Description |
|---|---|
| `pi auth check` | Print `ready`, `not_ready`, or `invalid`; exit with status `0`, `1`, or `2`, respectively |
| `pi auth print-api-key` | Print the resolved API key |
| `pi auth print-bearer-token` | Print a resolved OAuth bearer token |

| Option | Applies to | Description |
|---|---|---|
| `--provider <provider>` | All | Resolve credentials for a provider |
| `--model <model>` | All | Resolve credentials from a model; may be combined with `--provider` |
| `--json` | `auth check` | Write the structured result as JSON |
| `--credentials` | `auth check` | Emit the resolved credential when ready |
| `--no-refresh` | `auth check` | Do not refresh expired OAuth credentials; refresh is the default |
| `--min-expiry <duration>` | `print-bearer-token` | Require remaining token lifetime using `ms`, `s`, `m`, or `h`, such as `30m` |

Credential-printing commands write secrets to stdout.

## MCP commands

These commands work outside a session, so agents can run them through `bash`. See [MCP Servers](../03-customize-pi/06-mcp.md).

| Command | Description |
|---|---|
| `pi mcp add <server> [options] -- <command> [args...]` | Add or replace a stdio server in `mcp.json`; `--env KEY=VALUE` (repeatable) and `--cwd <dir>` set its environment and working directory. Arguments after the command are passed to it |
| `pi mcp add <server> [options] --url <url>` | Add or replace a streamable HTTP server; `--header KEY=VALUE` (repeatable), `--bearer-token-env-var <NAME>` (sends `Authorization: Bearer ${NAME}`), `--oauth-client-id`, `--oauth-client-secret`, `--oauth-callback-port`, and `--oauth-client-name` configure authentication |
| `pi mcp remove <server>` | Remove a server from `mcp.json`; stored OAuth credentials are kept |
| `pi mcp list [--json]` | Connect to every enabled server and print its state, tools, and errors; exit with `1` when a config entry is invalid or an enabled server is not connected |
| `pi mcp login <server> [--timeout <seconds>]` | Sign in to an OAuth server: open the authorization page and wait for the browser (default 300 seconds); a terminal also accepts the pasted redirect URL |
| `pi mcp logout <server>` | Delete the stored OAuth credentials of a server |

`add` and `remove` change `~/.pi/agent/mcp.json`, or `.pi/mcp.json` in the current directory with `--local` (`-l`). `add` also takes `--exposure <mode>` (see [Exposure](../03-customize-pi/06-mcp.md#exposure)) and `--description <text>` and does not connect; run `pi mcp list` to check the server.

Project `.pi/mcp.json` files are only read for projects that are already trusted.


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/02-codemode.md -->
<!-- ============================================================ -->

# Codemode

The `codemode` tool lets the model write a JavaScript script that calls pi's other tools and runs non-LLM models, such as classifiers and image models. Only the script's output reaches the model, so a script can run calls in parallel and filter large results before the model sees them. To turn it on, see [Enable codemode](../05-reference/01-cli.md#enable-codemode).

## Scripts

The tool input is raw JavaScript source, not JSON and not a markdown code fence. It runs as the body of an async function in a QuickJS sandbox, so top-level `await` and `return` work. The sandbox has no Node APIs, file system, network, or timers; scripts reach the outside world only through tools and `models`.

A script may start with an options line:

```js
// @options: {"max_output_tokens": 2000, "timeout_ms": 60000}
```

- `max_output_tokens` (default 10000) limits the output. Longer output keeps its start and end, and the full text is written to a temp file whose path is included in the result. A script fails when its output passes 16777216 characters of text and base64 image data or 100000 `text()`, `image()`, and `console` calls; write large data to a file with a tool instead.
- `timeout_ms` is a hard deadline for the whole script. It is unset by default. Image generation can take minutes, so do not set a short deadline for scripts that generate images.

The result starts with `Script completed` or `Script failed`, the wall time, and the output. A failed script keeps its partial output, followed by `Script error:` and the error. Tool calls are real: calls made before a failure are not undone. Calls still running when the script ends are cancelled, and unawaited promises are discarded.

## Globals

| Global | Purpose |
|---|---|
| `tools.<name>(args)` | Call a tool. See [Call tools](#call-tools). |
| `text(value)` | Add a text item to the output. Strings are added as is, other values as JSON. |
| `image(value)` | Add an image to the output: a base64 `data:` URL, an `{ image_url }` object, or an image block `{ type: "image", data, mimeType }` such as those returned by MCP tools and `models.generateImages()`. Remote URLs are not supported. PNG, JPEG, GIF, and WebP are accepted. |
| `console.log(...)` | Like `text()`; `info`, `warn`, `error`, and `debug` do the same. |
| `return value` | A top-level `return` adds the value like `text()`. |
| `exit()` | End the script successfully. |
| `store(key, value)` / `load(key)` | Keep small JSON values across `codemode` calls. See [Store values](#store-values). |
| `ALL_TOOLS` | Every callable tool as `{ name, description }`, including tools the description does not list. |
| `searchTools(query, { limit?, namespace? })` | Rank callable tools by relevance (BM25, default limit 8). Resolves to `{ name, description }[]`. |
| `describeTool(name)` | Resolves to a tool's description and TypeScript declaration, or `undefined`. |
| `describeNamespace(name)` | Resolves to `{ name, description?, instructions?, tools }` for a namespace such as an MCP server, or `undefined`. |
| `models` | List and run non-LLM models. See [Models](#models). |

## Call tools

Every tool the session can call is a method of `tools`, named by its identifier: characters that are not valid in a JavaScript identifier become `_`, so the MCP tool `mcp__dev-radius__search` is `tools.mcp__dev_radius__search`. Each method takes one object with the tool's arguments.

What a call resolves to depends on the tool:

- Tools with an output schema resolve to a structured value. `bash` resolves to `{ output, truncated, full_output_path?, exit_code, wall_time_seconds }`, also for non-zero exit codes. Its `output` is not limited to the 2000 lines or 50KB the model sees: it holds up to 1 MiB, and longer output keeps its first and last 512 KiB around an omission marker, with `truncated` set and the full output in `full_output_path`.
- MCP tools resolve to their `CallToolResult`, including `isError` and `structuredContent`.
- Other tools, such as `read`, `edit`, and `write`, resolve to their text output.

A call that fails, is blocked, or gets invalid arguments rejects with an `Error` that carries the tool's error text. Use `Promise.allSettled()` to keep the results of the calls that succeed.

The `codemode` description lists tools with their TypeScript declarations, grouped by namespace (for example one MCP server). Tools with `deferred` exposure, which includes MCP tools with the default `codemode` exposure, are not listed, so the description stays the same while MCP servers connect. Listed declarations share a budget of 3000 estimated tokens (`codemode.inlineBudget` in [settings](../05-reference/04-settings.md#tools)). Scripts find the other tools with `searchTools()`, `describeTool()`, `describeNamespace()`, or by filtering `ALL_TOOLS`.

While `codemode` is active, `codemode.mode` in [settings](../05-reference/04-settings.md#tools) decides how the other tools are presented. With `on` (default) declared tools stay declared, and their descriptions say how to call them from scripts. With `only` they are hidden from the model and listed in the `codemode` description instead, so the model calls them through scripts.

## Store values

`store(key, value)` keeps a JSON value under a string key for later `codemode` calls; storing `undefined` deletes the key. `load(key)` returns the value, or `undefined`. Writes are kept only when the script succeeds: each successful script that stores values appends a `codemode-store` custom entry to the session, so resumed sessions keep the values and each branch sees only the values written on its path.

The store is for small state such as IDs, cursors, or summaries. One value may have at most 262144 characters of JSON and all values together at most 1048576. Do not store image data; show images with `image()` or write them to a file with a tool.

## Models

`models` reaches the model catalog and runs non-LLM models with the session's credentials: classifiers, which answer typed questions about JSON state, and image models, which generate images. Chat models are listed but cannot be run from scripts. Which classifier and image models exist is described in [Use classifier models](../02-run-pi/02-models.md#use-classifier-models) and [Use image models](../02-run-pi/02-models.md#use-image-models).

```ts
type ModelType = "chat" | "image" | "classifier";

/** A catalog entry. `provider` and `id` identify it; other fields depend on the type. */
interface ModelInfo {
  type?: ModelType;
  provider: string;
  id: string;
  name: string;
  api: string;
  input: ("text" | "image")[];
  contextWindow?: number;
  [key: string]: unknown;
}

declare const models: {
  /** Every known model of a type, optionally for one provider. */
  getModelsOfType(type: ModelType, provider?: string): Promise<ModelInfo[]>;
  /** Models of a type whose provider has working credentials. */
  getAvailableOfType(type: ModelType, provider?: string): Promise<ModelInfo[]>;
  /** One catalog entry, or undefined. */
  getModelOfType(type: ModelType, provider: string, id: string): Promise<ModelInfo | undefined>;
  /** Answer `context.questions` about `context.state`; answers are in `result.answers` by question ID. */
  classify(model: ModelInfo, context: ClassifierContext): Promise<ClassifierResult>;
  /** Generate images from `context.input` text and image blocks; show `result.output` blocks with image(). Can take minutes. */
  generateImages(model: ModelInfo, context: ImagesContext): Promise<ImagesResult>;
};
```

`classify()` and `generateImages()` use only the `provider` and `id` of `model`, so `{ provider, id }` works as well. They do not throw on provider errors: check `stopReason` and `errorMessage`. At most four such calls run at once per script; more calls wait for a free slot, so `Promise.all()` over many items is fine. Their usage is added to the `codemode` tool result and counts toward the session cost.

Model IDs differ between providers, for example `typesafe/jev-latest` and `openrouter/typesafe/jev-1.13`. Use `models.getAvailableOfType(type)` to find the IDs that work with the current credentials.

### Classify

```ts
interface ClassifierContext {
  /** The data to classify. */
  state: Record<string, unknown>;
  /** Questions by ID. One call answers all of them. */
  questions: Record<string, ClassifierQuestion>;
}

type ClassifierQuestion =
  /** Pick one label. `criteria` maps each label to what it means. */
  | { type: "choice"; instructions: string; criteria: Record<string, string> }
  /** Score on an ordered scale. `criteria` describes each level, lowest first. */
  | { type: "score"; instructions: string; criteria: string[] }
  /** Yes or no. */
  | { type: "bool"; instructions: string; criteria: { true: string; false: string } };

interface ClassifierResult {
  provider: string;
  model: string;
  /** Answers by question ID. */
  answers: Record<string, ClassifierAnswer>;
  usage?: ModelUsage;
  stopReason: "stop" | "error" | "aborted";
  errorMessage?: string;
}

type ClassifierAnswer =
  | { type: "choice"; choice: string; probabilities: Record<string, number>; confidence: number }
  /** `score` is the expected level index, from 0 to `criteria.length - 1`. */
  | { type: "score"; score: number; confidence: number }
  /** Probability of `true`. */
  | { type: "bool"; probability: number };

/** Token counts and cost in USD, when the service reports them. */
type ModelUsage = { input: number; output: number; totalTokens: number; cost: { total: number } };
```

Classify several items by calling `classify()` once per item. This script sorts feedback messages, for example ones a tool returned earlier in the script:

```js
const jev = await models.getModelOfType("classifier", "typesafe", "jev-latest");
const results = await Promise.all(
  messages.map((message) =>
    models.classify(jev, {
      state: { message },
      questions: {
        sentiment: {
          type: "choice",
          instructions: "How does the user feel about the product?",
          criteria: { positive: "Satisfied or happy", negative: "Unhappy or frustrated", neutral: "Neither" },
        },
        urgency: {
          type: "score",
          instructions: "How urgently does this need a reply?",
          criteria: ["no reply needed", "reply this week", "reply today"],
        },
      },
    }),
  ),
);
return results.map((result, i) =>
  result.stopReason === "stop"
    ? { message: messages[i], sentiment: result.answers.sentiment.choice, urgency: result.answers.urgency.score }
    : { message: messages[i], error: result.errorMessage },
);
```

### Generate images

```ts
interface ImagesContext {
  /** The prompt as text blocks, plus image blocks to edit or use as references. */
  input: (TextBlock | ImageBlock)[];
}

interface ImagesResult {
  provider: string;
  model: string;
  /** Generated images, and text blocks for models that also return text. */
  output: (TextBlock | ImageBlock)[];
  usage?: ModelUsage;
  stopReason: "stop" | "error" | "aborted";
  errorMessage?: string;
}

type TextBlock = { type: "text"; text: string };
/** `data` is base64. */
type ImageBlock = { type: "image"; data: string; mimeType: string };
```

Show generated images with `image(block)`. Do not print `data` with `text()`, `console`, or `return`: it is large and the model cannot read it as text. Generated images are not saved to disk; to keep one, write it to a file with a tool.

```js
// @options: {"timeout_ms": 300000}
const painter = await models.getModelOfType("image", "openrouter", "google/gemini-2.5-flash-image");
const result = await models.generateImages(painter, {
  input: [{ type: "text", text: "A red fox in the snow, watercolor" }],
});
if (result.stopReason !== "stop") return result.errorMessage;
for (const block of result.output) {
  if (block.type === "image") image(block);
  else text(block.text);
}
```

## Limits

- A script's VM has 256 MB of memory. Running out throws `InternalError: out of memory`; filter or aggregate large data instead of accumulating it.
- A script that waits on a promise that can never settle (no tool call pending) fails immediately, since there are no timers.
- Scripts cannot start other `codemode` scripts.


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/03-slash-commands.md -->
<!-- ============================================================ -->

# Slash commands

Type `/` in Pi's terminal editor to search the commands available in the current session. This page lists the built-in commands in the current Pi release.

Extensions, prompt templates, and skills can add commands. The command menu in Pi is therefore the exact reference for the resources loaded in your session.

## Models and settings

| Command | Description |
|---|---|
| `/settings` | Open settings |
| `/model [provider/model]` | Select a model |
| `/thinking [level]` | Set the thinking level |
| `/scoped-models` | Configure the models used by interactive cycling |
| `/login [provider]` | Add provider authentication |
| `/logout` | Remove provider authentication |
| `/llama` | Manage models on the configured llama.cpp router |

## Sessions and context

| Command | Description |
|---|---|
| `/new` | Start a new session |
| `/resume` | Switch to another saved session |
| `/name [name]` | Set the session display name, or show the current name when omitted |
| `/session` | Show current session information and statistics |
| `/tree` | Navigate the session tree |
| `/fork` | Create a new session from an earlier user message |
| `/clone` | Duplicate the current session at its current position |
| `/compact [instructions]` | Compact the current context, optionally with custom instructions |
| `/import <path>` | Import and resume a JSONL session |

## Export and share

| Command | Description |
|---|---|
| `/copy` | Copy the last assistant message |
| `/export [path]` | Export the session as HTML or JSONL |
| `/share` | Upload the session and return a viewer link |
| `/bug [description]` | Prepare a private bug report for the Pi developers |

Review a session before exporting or sharing it. Sessions can contain prompts, tool arguments, command output, file contents, and credentials exposed during the conversation.

## Runtime and project

| Command | Description |
|---|---|
| `/trust` | Save a project trust decision for future Pi processes |
| `/reload` | Reload keybindings, extensions, skills, templates, themes, and context files |
| `/hotkeys` | Show active keyboard shortcuts |
| `/changelog` | Show changelog entries |
| `/quit` | Quit Pi |

## Commands added by resources

- Extensions can register commands with their own arguments and completion behavior.
- Each prompt template is available under its template name.
- Skills are available as `/skill:name` when skill commands are enabled.

Use `/reload` after adding or changing a discovered command resource. See [Extensions](../04-build-on-pi/01-extensions.md), [Prompt Templates](../03-customize-pi/02-prompt-templates.md), and [Skills](../03-customize-pi/03-skills.md) for their loading and naming rules.


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/04-settings.md -->
<!-- ============================================================ -->

# Settings Reference

This reference lists user-configurable settings, their types, defaults, and purposes. Project settings override agent-directory settings. Resource lists are combined. See [Configuration](../03-customize-pi/01-configuration.md) for file locations and trust behavior.

## Model and thinking

<a id="model-cycling"></a>

| Setting | Type | Default | Description |
|---|---|---|---|
| `defaultProvider` | string | Automatic | Startup AI provider. |
| `defaultModel` | string | Automatic | Startup model ID. |
| `defaultThinkingLevel` | `"off" \| "minimal" \| "low" \| "medium" \| "high" \| "xhigh" \| "max"` | `"medium"` | Startup thinking level. |
| `modelThinkingLevels` | object | None | Per-model startup thinking levels keyed by exact `provider/modelId`. |
| `thinkingBudgets` | object | Built-in budgets | Token budgets for `minimal`, `low`, `medium`, and `high` thinking levels. |
| `enabledModels` | `string[]` | All available models | Model patterns used for startup selection and model cycling. Uses the same format as `--models`. |
| `hideThinkingBlock` | boolean | `false` | Hide thinking blocks in the transcript. |
| `showCacheMissNotices` | boolean | `false` | Show notices for significant cache misses, successful cache warming, compaction usage, and provider recovery. |
| `cacheWarming` | `"off" \| "streaming" \| "idle"` | `"streaming"` | Keep eligible provider prompt caches warm during active runs or, with `"idle"`, between runs. Global setting only. |

Cache warming runs only when the model declares a cache lifetime and Pi estimates at least $0.05 in avoided cache-miss cost. Refresh usage counts toward session totals but does not enter model context. `/session` shows the next decision; extensions can override it with `cache_warming_decision`. See [Prompt Cache Lifetimes](../02-run-pi/02-models.md#prompt-cache-lifetimes).

See [Choose a Model](../02-run-pi/02-models.md) for model selection and thinking controls.

## Interaction

| Setting | Type | Default | Description |
|---|---|---|---|
| `steeringMode` | `"all" \| "one-at-a-time"` | `"one-at-a-time"` | How queued steering messages are delivered. |
| `followUpMode` | `"all" \| "one-at-a-time"` | `"one-at-a-time"` | How queued follow-up messages are delivered. |
| `externalEditor` | string | `$VISUAL`, `$EDITOR`, then platform default | Command opened by the external-editor keybinding. |
| `doubleEscapeAction` | `"tree" \| "fork" \| "none"` | `"tree"` | Action for double Escape with an empty editor. |
| `treeFilterMode` | `"default" \| "no-tools" \| "user-only" \| "labeled-only" \| "all"` | `"default"` | Initial filter used by `/tree`. |
| `defaultProjectTrust` | `"ask" \| "always" \| "never"` | `"ask"` | Fallback project-trust behavior. **Can only be set in agent-directory settings.** |

## Tools

| Setting | Type | Default | Description |
|---|---|---|---|
| `defaultTools` | `string[]` | `read`, `bash`, `edit`, `write` | Tools enabled at startup. Plain names replace the defaults; `+name` adds a tool and `-name` removes one. An empty array disables all built-in tools but not extension or SDK tools. |
| `codemode.mode` | `"on"` \| `"only"` | `"on"` | How the `codemode` tool presents tools while it is active. `on`: declared tools get a note on calling them from scripts appended to their description, and `codemode` lists only tools that are not declared. `only`: `codemode` lists every tool scripts can call, and active built-in and extension tools are hidden from the model, so it reaches them through `codemode`. |
| `codemode.inlineBudget` | number | `3000` | Estimated tokens (characters / 4) the `codemode` tool's description may spend on tool declarations. Tools that do not fit are left out and found with `searchTools()`. `0` lists only namespaces. |

Available built-in tools are `read`, `bash`, `powershell`, `edit`, `write`, `grep`, `find`, and `ls`. `defaultTools` can also name `codemode` and `tool_search`, which built-in extensions register inactive, and other extension tools registered inactive.

A list of only `+name` and `-name` entries changes the inherited selection instead of replacing it. For example, this enables `codemode` next to the default tools:

```json
{
  "defaultTools": ["+codemode"]
}
```

This replaces `bash` with `powershell` and enables `grep`: `["-bash", "+powershell", "+grep"]`. Project settings apply on top of user settings: a project list with only `+name` and `-name` entries changes the user's selection, and a project list with a plain name replaces it. In one list, plain names form the selection, and `+name` and `-name` then apply in order.

`/reload` enables tools newly added to `defaultTools`. It does not disable tools removed from it or re-enable unchanged tools you turned off. `--tools`, `--no-tools`, and `--no-builtin-tools` override `defaultTools`, also on reload.

CLI tool options override this setting for one invocation; `--tools` does not accept `+name` or `-name`. See [Command Line](../05-reference/01-cli.md#tools).

## Sessions and context

| Setting | Type | Default | Description |
|---|---|---|---|
| `sessionDir` | string | Agent session directory | Session storage directory. Relative paths resolve from the working directory. `PI_CODING_AGENT_SESSION_DIR` and `--session-dir` override this setting. |

### Compaction

| Setting | Type | Default | Description |
|---|---|---|---|
| `compaction.enabled` | boolean | `true` | Enable automatic compaction. |
| `compaction.reserveTokens` | number | `16384` | Tokens reserved for the model response. |
| `compaction.keepRecentTokens` | number | `20000` | Recent tokens retained without summarization. |
| `compaction.modelOverrides` | object | None | Per-model token settings keyed by exact `provider/modelId`. |

<a id="per-model-compaction-overrides"></a>

Compaction token values must be non-negative safe integers. Each value resolves independently from the matching model override, then the ordinary compaction setting, then the built-in default. Project and user objects merge before model lookup.

See [Compaction Reference](../05-reference/09-compaction.md) for trigger, summarization, and validation behavior.

### Branch summaries

| Setting | Type | Default | Description |
|---|---|---|---|
| `branchSummary.reserveTokens` | number | `16384` | Tokens reserved when summarizing branch history. |
| `branchSummary.skipPrompt` | boolean | `false` | Skip the branch-summary prompt and default to no summary. |

## Terminal and display

| Setting | Type | Default | Description |
|---|---|---|---|
| `theme` | string | `"system"` | Built-in or custom theme name. `system` derives colors from the terminal theme. |
| `quietStartup` | boolean \| `"header"` | `false` | `true` hides the startup header and loaded-resource listing. `"header"` keeps the header (version and key hints) but hides the model scope line and loaded-resource listing. |
| `tuiMode` | `"regular" \| "fullscreen"` | `"fullscreen"` | Interactive terminal UI mode. |
| `fullscreenExitOutput` | `"transcript" \| "resume-hint"` | `"transcript"` | Output printed when fullscreen mode exits. |
| `fullscreenScrollbar` | `"auto" \| "always" \| "hidden"` | `"auto"` | Fullscreen transcript scrollbar behavior. |
| `fullscreenCopyOnSelect` | boolean | `true` | Copy selected text automatically in fullscreen mode. |
| `fullscreenWheelScrollLines` | `"auto"` \| number | `"auto"` | Lines per mouse-wheel event in fullscreen mode, from 1 to 100. `"auto"` moves one line per event in local macOS terminals, which already accelerate wheel and trackpad input; elsewhere, and over SSH, it speeds up fast wheel spins to at most 6 lines per event. Alt+wheel moves five times as far. |
| `editorPaddingX` | number | `0` | Horizontal editor padding from 0 to 3 cells. |
| `outputPad` | `0 \| 1` | `1` | Horizontal transcript padding. |
| `autocompleteMaxVisible` | number | `5` | Visible autocomplete entries, from 3 to 20. |
| `showHardwareCursor` | boolean | `false` | Show the terminal cursor while Pi positions it for input methods. |
| `terminal.showImages` | boolean | `true` | Display inline images when supported. |
| `terminal.imageWidthCells` | number | `60` | Preferred inline image width in terminal cells. |
| `terminal.clearOnShrink` | boolean | `false` | Clear empty rows when rendered content shrinks. |
| `terminal.showTerminalProgress` | boolean | `false` | Show OSC 9;4 progress in the terminal tab. |
| `terminal.hyperlinks` | `boolean \| "auto"` | `"auto"` | Override OSC 8 hyperlink detection. |
| `terminal.images` | `"kitty" \| "iterm2" \| "auto" \| false` | `"auto"` | Override inline-image protocol detection. |
| `terminal.trueColor` | `boolean \| "auto"` | `"auto"` | Override true-color detection. |
| `images.autoResize` | boolean | `true` | Resize images to at most 2000 by 2000 pixels before sending them to a model. |
| `images.blockImages` | boolean | `false` | Prevent images from being sent to models. |
| `markdown.codeBlockIndent` | string | `"  "` | Prefix used to indent rendered code blocks. |
| `markdown.mermaid` | `"off" \| "final" \| "streaming"` | `"streaming"` | Mermaid rendering mode. |

See [Themes](../03-customize-pi/04-themes.md) and [Terminal Setup](../02-run-pi/07-terminal-setup.md) for format and platform details.

## Network and retries

| Setting | Type | Default | Description |
|---|---|---|---|
| `transport` | `"auto" \| "sse" \| "websocket" \| "websocket-cached"` | `"auto"` | Preferred transport for AI providers that support multiple transports. |
| `httpProxy` | string | None | Proxy URL applied as `HTTP_PROXY` and `HTTPS_PROXY` for Pi-managed HTTP clients. **Can only be set in agent-directory settings.** |
| `httpIdleTimeoutMs` | number | `300000` | HTTP header and body idle timeout in milliseconds. Set to `0` to disable. |
| `websocketConnectTimeoutMs` | number | `15000` | WebSocket connection timeout in milliseconds. Set to `0` to disable. |
| `retry.enabled` | boolean | `true` | Enable automatic agent-level retry for transient failures. |
| `retry.maxRetries` | number | `3` | Maximum agent-level retry attempts. |
| `retry.baseDelayMs` | number | `2000` | Initial exponential-backoff delay in milliseconds. |
| `retry.maxAgentDelayMs` | number | `60000` | Maximum agent-level retry delay in milliseconds. |
| `retry.provider.timeoutMs` | number | `httpIdleTimeoutMs` | Provider request timeout in milliseconds. |
| `retry.provider.maxRetries` | number | `0` | Provider-level retry attempts. |
| `retry.provider.maxRetryDelayMs` | number | `60000` | Maximum server-requested delay in milliseconds. Set to `0` to disable the limit. |

Keep `retry.provider.maxRetries` at `0` unless provider-level retries are required. Provider retries can delay Pi from handling quota and usage-limit errors itself.

## Shell

| Setting | Type | Default | Description |
|---|---|---|---|
| `shellPath` | string | Platform default | Custom shell executable path. Supports a leading `~`. |
| `shellCommandPrefix` | string | None | Prefix prepended to every shell command. |
| `npmCommand` | `string[]` | `npm` | Command and arguments used for npm package lookup and installation. |

See [Shell aliases](../02-run-pi/08-shell-aliases.md) for shell setup and [Pi Packages](../03-customize-pi/05-packages.md) for package-manager behavior.

## Resources

Resource paths in user settings resolve from the agent directory. Paths in project settings resolve from the project `.pi` directory. Absolute paths and `~` are supported.

| Setting | Type | Default | Description |
|---|---|---|---|
| `packages` | array | `[]` | npm, git, or local Pi package sources. See [Pi Packages](../03-customize-pi/05-packages.md). |
| `extensions` | `string[]` | `[]` | Extension files or directories. |
| `skills` | `string[]` | `[]` | Skill files or directories. |
| `prompts` | `string[]` | `[]` | Prompt-template files or directories. |
| `themes` | `string[]` | `[]` | Theme files or directories. |
| `enableSkillCommands` | boolean | `true` | Register skills as `/skill:name` commands. |

Resource arrays support glob exclusions with `!pattern`, exact inclusion with `+path`, and exact exclusion with `-path`. Pi loads resources listed in both user-level and project settings.

The built-in extensions are named `builtin:mcp`, `builtin:llama.cpp`, `builtin:codemode`, and `builtin:tool-search` in `extensions`. They load by default; `-builtin:mcp` disables one. A `+builtin:<name>` or `-builtin:<name>` entry in project settings overrides the user setting. `pi config` lists them under Built-in. `--no-extensions` disables them too, and `-e builtin:<name>` loads one explicitly.

## Updates, telemetry, and warnings

| Setting | Type | Default | Description |
|---|---|---|---|
| `collapseChangelog` | boolean | `false` | Show a condensed changelog after an update. |
| `enableInstallTelemetry` | boolean | `true` | Enable anonymous install/update reporting and selected provider attribution headers. Does not control update checks. |
| `enableAnalytics` | boolean | `false` | Opt in to analytics data sharing. Currently used only by the experimental first-run setup. |
| `warnings.anthropicExtraUsage` | boolean | `true` | Warn when Anthropic subscription authentication may use paid extra usage. |


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/05-environment-variables.md -->
<!-- ============================================================ -->

# Environment Variables

Pi uses environment variables in three ways:

- Variables such as `PI_OFFLINE` configure the Pi process.
- Pi sets process markers so child processes can identify Pi as the launching agent.
- Commands run by the LLM-callable shell tools receive `PI_*` variables describing the current session.

Provider API-key variables are documented separately in [Providers](../05-reference/07-providers.md#use-an-api-key-from-the-environment).

## Process Marker

The CLI and RPC entry points set two process markers:

- `AI_AGENT=pi` is a generic marker that lets tooling identify Pi as the agent that launched the process.
- `PI_CODING_AGENT=true` is Pi-specific and lets child processes detect that they run inside Pi.

Child processes inherit both markers. They are not session-specific and are not set automatically when Pi is embedded through the SDK.

## Shell Tool Session Environment

Commands run by the `bash` and `powershell` tools receive the current Pi session state:

| Variable | Description |
|----------|-------------|
| `PI_SESSION_ID` | Current session ID |
| `PI_SESSION_FILE` | Absolute path to the current session JSONL file; unset for ephemeral sessions |
| `PI_PROVIDER` | Currently selected model provider |
| `PI_MODEL` | Currently selected model ID |
| `PI_REASONING_LEVEL` | Current effective reasoning level: `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, or `max` |

The values are resolved when each command starts. Switching models or changing the reasoning level therefore affects the next shell command without restarting Pi. `PI_PROVIDER` and `PI_MODEL` identify the selected Pi model, not a different upstream model that a router may choose internally.

When asked which model or provider is running, inspect these variables instead of inferring the answer from the system prompt:

```bash
printf '%s/%s\n' "$PI_PROVIDER" "$PI_MODEL"
printf 'reasoning=%s session=%s\n' "$PI_REASONING_LEVEL" "$PI_SESSION_ID"
```

The session file can be inspected directly when the session is persistent:

```bash
if [ -n "$PI_SESSION_FILE" ]; then
  tail -n 1 "$PI_SESSION_FILE"
fi
```

These variables are injected into the LLM-callable `bash` and `powershell` tools. They are not injected into user-entered `!` or `!!` commands.

### Custom Shell Tools

Tools created with `createBashTool()` or `createPowerShellTool()` expose the session environment by default when registered with Pi. Injection happens before `spawnHook`, so a hook receives the variables in `ctx.env`:

```typescript
const bashTool = createBashTool(cwd, {
  spawnHook: (ctx) => ({
    ...ctx,
    env: { ...ctx.env, CI: "1" },
  }),
});
```

Disable session metadata independently of the spawn hook:

```typescript
const powershellTool = createPowerShellTool(cwd, {
  exposeSessionEnvironment: false,
  spawnHook: (ctx) => ctx,
});
```

When disabled, Pi removes inherited values for these variables so nested Pi processes do not expose stale parent-session metadata.

## Pi Process Configuration

These variables are read by Pi itself:

| Variable | Description |
|----------|-------------|
| `PI_CODING_AGENT_DIR` | Override the config directory; default is `~/.pi/agent` |
| `PI_CODING_AGENT_SESSION_DIR` | Override session storage; overridden by `--session-dir` |
| `PI_PACKAGE_DIR` | Override the package directory, useful for Nix/Guix store paths |
| `PI_OFFLINE` | Disable automatic network activity, including model catalog refreshes |
| `PI_SKIP_VERSION_CHECK` | Disable the `pi.dev` latest-version request |
| `PI_TELEMETRY` | Override install/update telemetry and provider attribution headers: `1`/`true`/`yes` or `0`/`false`/`no` |
| `PI_CACHE_RETENTION` | Set to `long` for extended provider prompt caching where supported |
| `PI_SHARE_VIEWER_URL` | Override the base URL used by `/share` |
| `PI_RADIUS_GATEWAY` | Override the Radius gateway origin used by `/bug` uploads and Radius relay connections |
| `PI_HARDWARE_CURSOR` | Set to `1` to show the hardware cursor; see [Terminal setup](../02-run-pi/07-terminal-setup.md) |
| `PI_HYPERLINKS` | Override OSC 8 hyperlink detection with `1`, `0`, or `auto` |
| `PI_IMAGE_PROTOCOL` | Override inline image detection with `kitty`, `iterm2`, `none`, or `auto` |
| `PI_TRUE_COLOR` | Override truecolor detection with `1`, `0`, or `auto` |
| `PI_TUI_ESC_TIMEOUT` | How long to wait after a lone ESC before treating it as Escape, in milliseconds; defaults to `100` over SSH and `10` otherwise. Increase if Alt-key input is misread as Escape |
| `VISUAL`, `EDITOR` | External editor fallback when `externalEditor` is unset |
| `HTTP_PROXY`, `HTTPS_PROXY` | Proxy outbound HTTP requests |

Provider credentials such as `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, and provider-specific configuration are listed in [Providers](../05-reference/07-providers.md#use-an-api-key-from-the-environment).


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/06-keybindings.md -->
<!-- ============================================================ -->

# Keybindings Reference

Pi exposes named actions, such as `app.session.new`, that can be assigned keybindings. You can change default assignments or bind unassigned actions in Pi's [user configuration](../03-customize-pi/01-configuration.md#agent-directory).

Run `/hotkeys` to see the active shortcuts for the main editor and application.

## Assign keybindings

Create `<agent-dir>/keybindings.json`. The agent directory defaults to `~/.pi/agent` and is described in [Agent directory](../03-customize-pi/01-configuration.md#agent-directory).

Map each action identifier to one key or a list of keys:

```json
{
  "app.session.new": "ctrl+shift+n",
  "app.session.tree": ["ctrl+shift+t", "alt+shift+t"]
}
```

A configured value replaces the default for that action. Use an empty list to disable an action's keybindings:

```json
{
  "tui.altScreen.pageUp": []
}
```

After editing the file, run `/reload` to apply the changes to the active session.

## Key syntax

Write a key as `modifier+key`. Modifiers are `ctrl`, `shift`, `alt`, and `super`. You can combine modifiers. Valid keys are:

- **Letters:** `a-z`
- **Digits:** `0-9`
- **Special:** `escape`, `esc`, `enter`, `return`, `tab`, `space`, `backspace`, `delete`, `insert`, `clear`, `home`, `end`, `pageUp`, `pageDown`, `up`, `down`, `left`, `right`
- **Function:** `f1`-`f12`
- **Symbols:** `` ` ``, `-`, `=`, `[`, `]`, `\`, `;`, `'`, `,`, `.`, `/`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `(`, `)`, `_`, `+`, `|`, `~`, `{`, `}`, `:`, `<`, `>`, `?`

Examples: `ctrl+shift+x`, `alt+ctrl+x`, `ctrl+shift+alt+x`, `super+k`, `ctrl+super+k`, and `ctrl+1`.

`super` bindings require a terminal that reports the modifier separately, typically through the Kitty keyboard protocol. They may not work in terminals without that support.

## Actions

### Terminal UI

#### Cursor movement

| Keybinding id | Default | Description |
|---|---|---|
| `tui.editor.cursorUp` | `up` | Move cursor up, browsing older history at the top |
| `tui.editor.cursorDown` | `down` | Move cursor down, browsing newer history at the bottom |
| `tui.editor.historyPrevious` | None | Select the previous prompt history entry |
| `tui.editor.historyNext` | None | Select the next prompt history entry |
| `tui.editor.cursorLeft` | `left`, `ctrl+b` | Move cursor left |
| `tui.editor.cursorRight` | `right`, `ctrl+f` | Move cursor right |
| `tui.editor.cursorWordLeft` | `alt+left`, `ctrl+left`, `alt+b` | Move cursor word left |
| `tui.editor.cursorWordRight` | `alt+right`, `ctrl+right`, `alt+f` | Move cursor word right |
| `tui.editor.cursorLineStart` | `home`, `ctrl+home`, `ctrl+a` | Move to line start |
| `tui.editor.cursorLineEnd` | `end`, `ctrl+end`, `ctrl+e` | Move to line end |
| `tui.editor.jumpForward` | `ctrl+]` | Jump forward to character |
| `tui.editor.jumpBackward` | `ctrl+alt+]` | Jump backward to character |
| `tui.editor.pageUp` | `pageUp`, `ctrl+pageUp` | Scroll up by page |
| `tui.editor.pageDown` | `pageDown`, `ctrl+pageDown` | Scroll down by page |

The dedicated history actions browse prompt history regardless of cursor position and take precedence over application actions using the same key.

#### Text editing

| Keybinding id | Default | Description |
|---|---|---|
| `tui.editor.deleteCharBackward` | `backspace` | Delete character backward |
| `tui.editor.deleteCharForward` | `delete`, `ctrl+d` | Delete character forward |
| `tui.editor.deleteWordBackward` | `ctrl+w`, `alt+backspace` | Delete word backward |
| `tui.editor.deleteWordForward` | `alt+d`, `alt+delete` | Delete word forward |
| `tui.editor.deleteToLineStart` | `ctrl+u` | Delete to line start |
| `tui.editor.deleteToLineEnd` | `ctrl+k` | Delete to line end |
| `tui.editor.yank` | `ctrl+y` | Paste most recently deleted text |
| `tui.editor.yankPop` | `alt+y` | Cycle through deleted text after yank |
| `tui.editor.undo` | `ctrl+-` (`ctrl+z` on Windows; `alt+z` on WSL) | Undo last edit |

#### Input and selection

| Keybinding id | Default | Description |
|---|---|---|
| `tui.input.newLine` | `shift+enter`, `ctrl+j` | Insert new line |
| `tui.input.submit` | `enter` | Submit input |
| `tui.input.tab` | `tab` | Tab or autocomplete |
| `tui.input.copy` | `ctrl+c` | Copy selection |
| `tui.select.up` | `up` | Move selection up |
| `tui.select.down` | `down` | Move selection down |
| `tui.select.pageUp` | `pageUp` | Page up in list |
| `tui.select.pageDown` | `pageDown` | Page down in list |
| `tui.select.confirm` | `enter` | Confirm selection |
| `tui.select.cancel` | `escape`, `ctrl+c` | Cancel selection |

#### Fullscreen

In fullscreen mode, these actions control the transcript and take precedence over editor actions using the same key.

| Keybinding id | Default | Description |
|---|---|---|
| `tui.altScreen.pageUp` | `pageUp` | Scroll the transcript up by one page |
| `tui.altScreen.pageDown` | `pageDown` | Scroll the transcript down by one page |
| `tui.altScreen.halfPageUp` | None | Scroll the transcript up by half a page |
| `tui.altScreen.halfPageDown` | None | Scroll the transcript down by half a page |
| `tui.altScreen.lineUp` | None | Scroll the transcript up by one line |
| `tui.altScreen.lineDown` | None | Scroll the transcript down by one line |
| `tui.altScreen.previousPrompt` | `ctrl+shift+up`, `ctrl+up` (`ctrl+up` only on Windows and WSL) | Jump to the previous marked message |
| `tui.altScreen.nextPrompt` | `ctrl+shift+down`, `ctrl+down` (`ctrl+down` only on Windows and WSL) | Jump to the next marked message |
| `tui.altScreen.search` | `ctrl+shift+f` (`ctrl+f` on Windows and WSL) | Search the rendered transcript |
| `tui.altScreen.searchNext` | `enter`, `ctrl+g` | Select the next search match while searching |
| `tui.altScreen.searchPrevious` | `shift+enter`, `ctrl+shift+g` | Select the previous search match while searching |
| `tui.altScreen.searchClose` | `escape` | Close transcript search |
| `tui.altScreen.top` | `home` | Scroll to the beginning of the transcript |
| `tui.altScreen.bottom` | `end` | Scroll to the transcript end and follow new output |

### Application

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.interrupt` | `escape` | Cancel / abort |
| `app.clear` | `ctrl+c` | Clear editor (first) / exit (second) |
| `app.exit` | `ctrl+d` | Exit (when editor empty) |
| `app.suspend` | `ctrl+z` (None on Windows) | Suspend to background |
| `app.editor.external` | `ctrl+g` | Open in external editor (`externalEditor`, `$VISUAL`, `$EDITOR`, Notepad on Windows, or `nano` elsewhere) |
| `app.clipboard.pasteImage` | `ctrl+v` (`alt+v` on Windows and WSL) | Paste files on macOS, images, or text from clipboard |

On native Windows, `app.suspend` has no default because Windows terminals do not support Unix job control. If you assign it manually, Pi shows a status message instead of suspending. WSL uses the normal `ctrl+z` and `fg` behavior.

### Sessions

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.session.new` | None | Start a new session (`/new`) |
| `app.session.tree` | None | Open session tree navigator (`/tree`) |
| `app.session.fork` | None | Fork current session (`/fork`) |
| `app.session.resume` | None | Open session resume picker (`/resume`) |
| `app.session.togglePath` | `ctrl+p` | Toggle path display |
| `app.session.toggleSort` | `ctrl+s` | Toggle sort mode |
| `app.session.toggleNamedFilter` | `ctrl+n` | Toggle named-only filter |
| `app.session.rename` | `ctrl+r` | Rename session |
| `app.session.delete` | `ctrl+d` | Delete session |
| `app.session.deleteNoninvasive` | `ctrl+backspace` | Delete session when query is empty |

### Models and Thinking

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.model.select` | `ctrl+l` | Open model selector |
| `app.model.cycleForward` | `ctrl+p` | Cycle to next model |
| `app.model.cycleBackward` | `shift+ctrl+p` (`alt+p` on Windows and WSL) | Cycle to previous model |
| `app.models.save` | `ctrl+s` | Save the selected default model or scoped model configuration to settings |
| `app.thinking.cycle` | `shift+tab` | Cycle thinking level |
| `app.thinking.save` | `ctrl+s` | Save current thinking level to settings |
| `app.thinking.toggle` | `ctrl+t` | Collapse or expand thinking blocks |

### Display and Message Queue

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.tools.expand` | `ctrl+o` | Collapse or expand tool output |
| `app.message.copy` | `ctrl+x` | Copy the selected message in `/tree`; in fullscreen mode, copy the active selection when `fullscreenCopyOnSelect` is `false`; otherwise copy the last assistant message. On OAuth sign-in screens, copy the sign-in URL |
| `app.message.followUp` | `alt+enter` (`ctrl+q` on Windows and WSL) | Queue follow-up message |
| `app.message.dequeue` | `alt+up` (`alt+q` on Windows and WSL) | Restore queued messages to editor |

### Tree Navigation

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.tree.foldOrUp` | `ctrl+left`, `alt+left` | Fold current branch segment, or jump to the previous segment start |
| `app.tree.unfoldOrDown` | `ctrl+right`, `alt+right` | Unfold current branch segment, or jump to the next segment start or branch end |
| `app.tree.editLabel` | `shift+l` | Edit the label on the selected tree node |
| `app.tree.toggleLabelTimestamp` | `shift+t` | Toggle label timestamps in the tree |
| `app.tree.filter.default` | `ctrl+d` | Set tree filter to default view |
| `app.tree.filter.noTools` | `ctrl+t` | Toggle tree filter that hides tool results |
| `app.tree.filter.userOnly` | `ctrl+u` | Toggle tree filter that shows only user messages |
| `app.tree.filter.labeledOnly` | `ctrl+l` | Toggle tree filter that shows only labeled entries |
| `app.tree.filter.all` | `ctrl+a` | Toggle tree filter that shows all entries |
| `app.tree.filter.cycleForward` | `ctrl+o` | Cycle tree filter forward |
| `app.tree.filter.cycleBackward` | `shift+ctrl+o` | Cycle tree filter backward |

### Scoped Models Selector

Used inside the scoped models selector (opened via `/scoped-models`).

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.models.enableAll` | `ctrl+a` | Enable all models (or all matching the current search) |
| `app.models.clearAll` | `ctrl+x` | Clear all models (or all matching the current search) |
| `app.models.toggleProvider` | `ctrl+p` | Toggle all models for the current provider |
| `app.models.reorderUp` | `alt+up` | Move the selected model up in the cycle order |
| `app.models.reorderDown` | `alt+down` | Move the selected model down in the cycle order |


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/07-providers.md -->
<!-- ============================================================ -->

# Providers

Most hosted providers support one or both of these authentication methods:

- Sign in through a browser or device flow backed by OAuth.
- Provide an API key.

Use `/login [provider]` to see the methods supported by a provider. Amazon Bedrock and Google Vertex AI can also use ambient cloud credentials.

## Authenticate interactively

Run `/login` and select a provider. Pi guides you through its OAuth or API-key flow and saves the resulting credential in [`auth.json`](../03-customize-pi/01-configuration.md#agent-directory).

On a remote or headless machine, an OAuth callback may not reach the local process. When prompted, paste the final redirect URL or authorization code back into Pi.

Run `/logout` and select a provider to remove its stored credential. This does not unset environment variables, remove authentication from `models.json`, or revoke the credential at the provider.

`auth.json` can contain API keys and OAuth tokens. Keep it private and do not commit it.

## Use an API key from the environment

Environment variables are useful in CI and anywhere Pi should not store the key. Set the variable before starting Pi:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
pi
```

This table covers providers with a single primary API-key variable. Providers that need additional configuration or support ambient credentials are covered under [Provider Specific Config](#provider-specific-config).

| Provider | Environment variable |
|---|---|
| Anthropic | `ANTHROPIC_API_KEY` |
| Ant Ling | `ANT_LING_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| NVIDIA NIM | `NVIDIA_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` |
| GitHub Copilot | `COPILOT_GITHUB_TOKEN` |
| Mistral | `MISTRAL_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Cerebras | `CEREBRAS_API_KEY` |
| xAI | `XAI_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Vercel AI Gateway | `AI_GATEWAY_API_KEY` |
| ZAI Coding Plan (Global) | `ZAI_API_KEY` |
| ZAI Coding Plan (China) | `ZAI_CODING_CN_API_KEY` |
| OpenCode Zen and Go | `OPENCODE_API_KEY` |
| Radius | `RADIUS_API_KEY` |
| TypeSafe ([classifier models](../02-run-pi/02-models.md#use-classifier-models)) | `TYPESAFE_API_KEY` |
| Hugging Face | `HF_TOKEN` |
| Fireworks | `FIREWORKS_API_KEY` |
| Together AI | `TOGETHER_API_KEY` |
| Baseten | `BASETEN_API_KEY` |
| Kimi For Coding | `KIMI_API_KEY` |
| Meta | `META_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |
| MiniMax (China) | `MINIMAX_CN_API_KEY` |
| Moonshot AI (Global and China) | `MOONSHOT_API_KEY` |
| Qwen Token Plan and Individual | `QWEN_TOKEN_PLAN_API_KEY` |
| Qwen Token Plan (China) | `QWEN_TOKEN_PLAN_CN_API_KEY` |
| Xiaomi MiMo | `XIAOMI_API_KEY` |
| Xiaomi MiMo Token Plan (China) | `XIAOMI_TOKEN_PLAN_CN_API_KEY` |
| Xiaomi MiMo Token Plan (Amsterdam) | `XIAOMI_TOKEN_PLAN_AMS_API_KEY` |
| Xiaomi MiMo Token Plan (Singapore) | `XIAOMI_TOKEN_PLAN_SGP_API_KEY` |

Anthropic also recognizes `ANTHROPIC_OAUTH_TOKEN` as an API credential and `ANTHROPIC_AUTH_TOKEN` as bearer authentication.

With no key or token set, Anthropic uses workload identity federation when `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID` and `ANTHROPIC_IDENTITY_TOKEN_FILE` are set: the Anthropic SDK exchanges the identity token for a short-lived access token and refreshes it itself (re-reading the identity token file, so keep that file fresh for long sessions). `ANTHROPIC_SERVICE_ACCOUNT_ID` and `ANTHROPIC_WORKSPACE_ID` are passed through when set.

## Load an API key from a command

To use a secret manager without writing the resolved key to disk, set a provider's `key` in `auth.json` to a command prefixed with `!`:

```json
{
  "anthropic": {
    "type": "api_key",
    "key": "!security find-generic-password -ws 'anthropic'"
  }
}
```

Pi runs the command when the key is first needed and caches its standard output for the process lifetime. Empty output, a timeout, or a nonzero exit leaves the key unresolved until Pi restarts.

## Provider Specific Config

The providers below have additional setup, need additional settings, or can use credentials supplied by their platform.

A stored API-key credential can include an `env` object. Its values take priority over the process environment for that provider:

```json
{
  "cloudflare-workers-ai": {
    "type": "api_key",
    "key": "...",
    "env": {
      "CLOUDFLARE_ACCOUNT_ID": "account-id"
    }
  }
}
```

### Radius

Radius is a service crafted for Pi by the builders of Pi, Earendil Works. It provides a customizable AI gateway with organization-level controls and analytics built in, and artifacts for sharing what you create with Pi.

To get started, run `/login radius` in Pi. This adds Radius as a provider, and its models appear in `/model` like any other provider's.

Radius also has an MCP server, so Pi can manage Radius for you.

Radius is currently in early alpha and evolving quickly. See [radius.earendil.com](https://radius.earendil.com) for more.

Radius authentication uses its gateway catalog and caches refreshed model metadata for later offline startup. A custom Radius gateway configured in `models.json` uses its own catalog rather than inheriting the public `radius.pi.dev` catalog.

### Azure OpenAI

Set an API key plus either a base URL or resource name:

```bash
export AZURE_OPENAI_API_KEY=...
export AZURE_OPENAI_BASE_URL=https://your-resource.ai.azure.com
# Or:
export AZURE_OPENAI_RESOURCE_NAME=your-resource
```

Resource root URLs under `ai.azure.com`, `cognitiveservices.azure.com`, and `openai.azure.com` are normalized to the OpenAI API path.

### Amazon Bedrock

Bedrock can use a bearer token or an ambient AWS credential source:

```bash
# Named profile
export AWS_PROFILE=your-profile

# IAM keys
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
# Required for temporary credentials
export AWS_SESSION_TOKEN=...

# Bedrock bearer token
export AWS_BEARER_TOKEN_BEDROCK=...

# Region, when not supplied by the profile or AWS SDK configuration
export AWS_REGION=us-west-2
# AWS_DEFAULT_REGION is also supported
```

Pi also supports ECS task credentials and IRSA through the standard `AWS_CONTAINER_CREDENTIALS_*` and `AWS_WEB_IDENTITY_TOKEN_FILE` variables.

### Cloudflare AI Gateway

The gateway requires a token, account ID, and gateway ID:

```bash
export CLOUDFLARE_API_KEY=...
export CLOUDFLARE_ACCOUNT_ID=...
export CLOUDFLARE_GATEWAY_ID=...
```

The account and gateway IDs can come from the process environment or the credential's `env` object in `auth.json`.

`CLOUDFLARE_API_KEY` authenticates Pi to the gateway. Upstream access can use Cloudflare unified billing, credentials stored in the gateway, or an `Authorization` header configured for the provider in `models.json`.

### Cloudflare Workers AI

Workers AI requires a token and account ID:

```bash
export CLOUDFLARE_API_KEY=...
export CLOUDFLARE_ACCOUNT_ID=...
```

The account ID can also be stored in the credential's `env` object.

### Google Vertex AI

Use a Google Cloud API key:

```bash
export GOOGLE_CLOUD_API_KEY=...
```

To use Application Default Credentials, configure a project and location:

```bash
export GOOGLE_CLOUD_PROJECT=your-project
# GCLOUD_PROJECT is also supported
export GOOGLE_CLOUD_LOCATION=us-central1
```

Then authenticate:

```bash
gcloud auth application-default login
```

To use a service-account key file instead, set `GOOGLE_APPLICATION_CREDENTIALS` along with the project and location.


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/08-session-format.md -->
<!-- ============================================================ -->

# Session File Format

Sessions are stored as JSONL (JSON Lines) files. Each line is a JSON object with a `type` field. Session entries form a tree structure via `id`/`parentId` fields, enabling in-place branching without creating new files.

For programmatic creation, persistence, and tree navigation, see the [`SessionManager` API](../04-build-on-pi/06-sdk.md#sessionmanager-api).


## File Location

```
~/.pi/agent/sessions/--<path>--/<timestamp>_<session-id>.jsonl
```

By default, `<session-id>` is a UUID. Callers can supply a custom ID through the SDK or `--session-id`. For `<path>`, Pi removes the leading path separator and replaces `/`, `\\`, and `:` with `-`.

## Deleting Sessions

Sessions can be removed by deleting their `.jsonl` files under `~/.pi/agent/sessions/`.

Pi also supports deleting sessions interactively from `/resume` (select a session and press `Ctrl+D`, then confirm). When available, pi uses the `trash` CLI to avoid permanent deletion.

## Session Version

Sessions have a version field in the header:

- **Version 1**: Linear entry sequence (legacy, auto-migrated on load)
- **Version 2**: Tree structure with `id`/`parentId` linking
- **Version 3**: Renamed `hookMessage` role to `custom` (extensions unification)

Existing sessions are automatically migrated to the current version (v3) when loaded.

## Source Files

Source on GitHub ([pi](https://github.com/earendil-works/pi)):
- [`packages/coding-agent/src/core/session-manager.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/session-manager.ts) - Session entry types and SessionManager
- [Message Types](../05-reference/14-message-types.md) - Shared message and content-block reference
- [`packages/coding-agent/src/core/messages.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/messages.ts) - Extended message types
- [`packages/ai/src/types.ts`](https://github.com/earendil-works/pi/blob/main/packages/ai/src/types.ts) - Base message and content-block types
- [`packages/agent/src/types.ts`](https://github.com/earendil-works/pi/blob/main/packages/agent/src/types.ts) - Extensible `AgentMessage` union

For TypeScript definitions in your project, inspect `node_modules/@earendil-works/pi-coding-agent/dist/` and `node_modules/@earendil-works/pi-ai/dist/`.

## Messages

A `message` entry stores an [`AgentMessage`](../05-reference/14-message-types.md). Message content blocks, roles, usage, and message timestamps are defined in [Message Types](../05-reference/14-message-types.md).

Session entry timestamps are ISO 8601 strings. The nested message timestamp is a Unix timestamp in milliseconds.

## Entry Base

All entries (except `SessionHeader`) extend `SessionEntryBase`:

```typescript
interface SessionEntryBase {
  type: string;
  id: string;           // Usually an 8-char hex ID; may fall back to a full UUID
  parentId: string | null;  // Parent entry ID (null for a root entry)
  timestamp: string;    // ISO timestamp
}
```

## Entry Types

### SessionHeader

First line of the file. Metadata only, not part of the tree (no `id`/`parentId`).

```json
{"type":"session","version":3,"id":"uuid","timestamp":"2024-12-03T14:00:00.000Z","cwd":"/path/to/project"}
```

For sessions with a parent (created via `/fork`, `/clone`, or `newSession({ parentSession })`):

```json
{"type":"session","version":3,"id":"uuid","timestamp":"2024-12-03T14:00:00.000Z","cwd":"/path/to/project","parentSession":"/path/to/original/session.jsonl"}
```

### SessionMessageEntry

A message in the conversation. The `message` field contains an `AgentMessage`. System messages carry the prompt and tool loadout: the first request of a session persists one with every prompt section and tool declaration, and later changes persist as system messages that patch `sections` by name (`null` removes one) and list `toolsAdded`/`toolsRemoved`. Replaying them in order yields the current prompt and tools; there is no separate prompt state entry.

```json
{"type":"message","id":"a0b1c2d3","parentId":null,"timestamp":"2024-12-03T14:00:00.000Z","message":{"role":"system","content":"","sections":{"preamble":"You are an expert coding assistant...","tools":"<tools>\n- read: ...\n</tools>","cwd":"/project"},"toolsAdded":[{"name":"read","description":"...","parameters":{}}],"timestamp":1733234400000}}
{"type":"message","id":"d4e5f6g7","parentId":"c3d4e5f6","timestamp":"2024-12-03T14:04:00.000Z","message":{"role":"system","content":"","sections":{"skills":"<skills>...</skills>"},"toolsRemoved":[{"name":"write"}],"timestamp":1733234640000}}
```

Sessions created before system messages existed have no leading system message; the first request declares the current prompt as a later system message, which replays the same way.

```json
{"type":"message","id":"a1b2c3d4","parentId":"prev1234","timestamp":"2024-12-03T14:00:01.000Z","message":{"role":"user","content":"Hello","timestamp":1733234401000}}
{"type":"message","id":"b2c3d4e5","parentId":"a1b2c3d4","timestamp":"2024-12-03T14:00:02.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Hi!"}],"api":"anthropic-messages","provider":"anthropic","model":"claude-sonnet-4-5","usage":{...},"stopReason":"stop","timestamp":1733234402000}}
{"type":"message","id":"c3d4e5f6","parentId":"b2c3d4e5","timestamp":"2024-12-03T14:00:03.000Z","message":{"role":"toolResult","toolCallId":"call_123","toolName":"bash","content":[{"type":"text","text":"output"}],"isError":false,"timestamp":1733234403000}}
```

Assistant messages name the model that produced them. Newer messages also record `thinkingLevel`, the Pi thinking level requested for that response.

### ModelChangeEntry

Emitted when the user switches models mid-session. The latest entry is the selected model, which may be a [virtual model](../04-build-on-pi/03-virtual-models.md); assistant messages then name the physical model that answered.

```json
{"type":"model_change","id":"d4e5f6g7","parentId":"c3d4e5f6","timestamp":"2024-12-03T14:05:00.000Z","provider":"openai","modelId":"gpt-4o"}
```

### ThinkingLevelChangeEntry

Emitted when the user changes the thinking/reasoning level.

```json
{"type":"thinking_level_change","id":"e5f6g7h8","parentId":"d4e5f6g7","timestamp":"2024-12-03T14:06:00.000Z","thinkingLevel":"high"}
```

### UsageEntry

Records model-attributed usage that is not an assistant message and does not participate in LLM context. `kind` is an arbitrary string identifying the operation; for example, cache warming uses `"cache_warm"`.

```json
{"type":"usage","id":"f6g7h8i9","parentId":"e5f6g7h8","timestamp":"2024-12-03T14:08:00.000Z","kind":"cache_warm","provider":"anthropic","model":"claude-sonnet-4-5","usage":{"input":0,"output":0,"cacheRead":50000,"cacheWrite":0,"totalTokens":50000,"cost":{"input":0,"output":0,"cacheRead":0.015,"cacheWrite":0,"total":0.015}}}
```

Usage entries contribute to session token and cost totals. Pi hides them from the conversation tree. Consumers should treat unknown `kind` values as normal usage rather than rejecting them.

### CompactionEntry

Created when context is compacted. Stores a summary of earlier messages and a complete system prompt/tool checkpoint.

```json
{"type":"compaction","id":"f6g7h8i9","parentId":"e5f6g7h8","timestamp":"2024-12-03T14:10:00.000Z","summary":"User discussed X, Y, Z...","firstKeptEntryId":"c3d4e5f6","tokensBefore":50000,"systemMessage":{"role":"system","content":"You are a coding assistant.","toolsAdded":[],"timestamp":1733235000000}}
```

`firstKeptEntryId` is required. It identifies the first entry retained from before the compaction entry. When rebuilding context, Pi replaces older summarized entries with the compaction summary and keeps the range beginning at this entry. A retain-none compaction stores its own ID in this field, so no preceding entries are retained.

Optional fields:
- `systemMessage`: The replayed prompt sections and tool declarations at the compaction boundary; it becomes the leading system message of the compacted context, and system messages among the kept entries are dropped in its favor. It is absent on older session entries.
- `usage`: LLM usage from generating the summary; included in session token and cost totals
- `details`: Implementation-specific data (e.g., `{ readFiles: string[], modifiedFiles: string[] }` for default, or custom data for extensions)
- `fromHook`: `true` if generated by an extension, `false`/`undefined` if pi-generated (legacy field name)

### ContextEditEntry

Append-only edit of one earlier context-producing entry. It changes only future model context; the target entry and its metadata remain unchanged in raw history, UI, exports, and session accounting.

```json
{"type":"context_edit","id":"g6h7i8j9","parentId":"f6g7h8i9","timestamp":"2024-12-03T14:11:00.000Z","targetId":"c3d4e5f6","replacement":null}
```

Targets may be user, assistant, tool-result, or custom-message entries. `replacement: null` omits the target from model context. A non-null `replacement` replaces only the target message content. String replacements for assistant and tool-result entries are normalized to one text block because those roles require content arrays. If several edits target the same entry, the latest edit on the active branch wins. Edits are branch-relative: navigating to a point before the edit reveals the target's original contribution again.

### BranchSummaryEntry

Created when switching branches via `/tree` with an LLM generated summary of the left branch up to the common ancestor. Captures context from the abandoned path.

```json
{"type":"branch_summary","id":"g7h8i9j0","parentId":"a1b2c3d4","timestamp":"2024-12-03T14:15:00.000Z","fromId":"f6g7h8i9","summary":"Branch explored approach A..."}
```

`parentId` is the entry from which the new branch continues. `fromId` is the previous leaf whose abandoned path was summarized.

Optional fields:
- `usage`: LLM usage from generating the summary; included in session token and cost totals
- `details`: File tracking data (`{ readFiles: string[], modifiedFiles: string[] }`) for default, or custom data for extensions
- `fromHook`: `true` if generated by an extension, `false`/`undefined` if pi-generated (legacy field name)

### CustomEntry

Extension state persistence. Does NOT participate in LLM context.

```json
{"type":"custom","id":"h8i9j0k1","parentId":"g7h8i9j0","timestamp":"2024-12-03T14:20:00.000Z","customType":"my-extension","data":{"count":42}}
```

Use `customType` to identify your extension's entries on reload. Interactive mode can render custom entries via `pi.registerEntryRenderer(customType, renderer)`, but they still do not participate in LLM context.

Pi stores [virtual model](../04-build-on-pi/03-virtual-models.md) router state as custom entries with `customType` `pi.virtual-model-state` and `data` `{ provider, modelId, state }`.

### CustomMessageEntry

Extension-injected messages that DO participate in LLM context.

```json
{"type":"custom_message","id":"i9j0k1l2","parentId":"h8i9j0k1","timestamp":"2024-12-03T14:25:00.000Z","customType":"my-extension","content":"Injected context...","display":true}
```

Fields:
- `content`: String or `(TextContent | ImageContent)[]` (same as UserMessage)
- `display`: `true` = show in TUI with distinct styling, `false` = hidden
- `details`: Optional extension-specific metadata (not sent to LLM)

### LabelEntry

User-defined bookmark/marker on an entry.

```json
{"type":"label","id":"j0k1l2m3","parentId":"i9j0k1l2","timestamp":"2024-12-03T14:30:00.000Z","targetId":"a1b2c3d4","label":"checkpoint-1"}
```

Set `label` to `undefined` to clear a label.

### SessionInfoEntry

Session metadata (e.g., user-defined display name). Set via `/name`, `--name` / `-n`, or `pi.setSessionName()` in extensions.

```json
{"type":"session_info","id":"k1l2m3n4","parentId":"j0k1l2m3","timestamp":"2024-12-03T14:35:00.000Z","name":"Refactor auth module"}
```

The session name is displayed in the session selector (`/resume`) instead of the first message when set.

## Tree Structure

Entries normally form one tree, but navigation APIs can create multiple roots:
- A root entry has `parentId: null`; the first entry is initially the root
- Each non-root entry points to its parent via `parentId`
- Branching creates new children from an earlier entry
- The "leaf" is the current position in the tree
- Calling `resetLeaf()` or `branchWithSummary(null, ...)` allows a later entry to become another root

```
[user msg] ─── [assistant] ─── [user msg] ─── [assistant] ─┬─ [user msg] ← current leaf
                                                            │
                                                            └─ [branch_summary] ─── [user msg] ← alternate branch
```

## Context Building

`buildContextEntries()` walks from the current leaf to the root, producing the active entry list while honoring compaction:

1. Collects all entries on the path
2. If one or more `CompactionEntry` values are on the path, uses the latest one:
   - Includes the compaction entry first
   - Includes non-system entries from `firstKeptEntryId` up to, but not including, the compaction entry
   - Includes entries after the compaction entry
3. Preserves non-message entries in the selected range so interactive mode can render them

`buildSessionProjection()` then applies the latest `context_edit` for each selected target. It returns the model-visible messages together with their source entries. Omitted targets produce no message; replacements retain the source entry's role and metadata while changing only content. The raw selected entries are not modified.

`buildSessionContext()` builds on that projection to produce the message list for the LLM:

1. Extracts current model and thinking level settings from the full path
2. Converts selected entries to messages:
   - `message` -> stored `AgentMessage`
   - `compaction` -> complete system checkpoint followed by `compactionSummary`
   - `branch_summary` -> `branchSummary`
   - `custom_message` -> `CustomMessage`
   - `context_edit` -> no context message of its own
   - `usage` and `custom` -> no context message

The compaction summary replaces entries before `firstKeptEntryId`. Pre-compaction system messages are folded into the complete checkpoint rather than replayed from the retained range. Retained non-system entries and all entries after the compaction remain available to the LLM.

## Parsing Example

```typescript
import { readFileSync } from "fs";

const lines = readFileSync("session.jsonl", "utf8").trim().split("\n");

for (const line of lines) {
  const entry = JSON.parse(line);

  switch (entry.type) {
    case "session":
      console.log(`Session v${entry.version ?? 1}: ${entry.id}`);
      break;
    case "message":
      console.log(`[${entry.id}] ${entry.message.role}: ${JSON.stringify(entry.message.content)}`);
      break;
    case "compaction":
      console.log(`[${entry.id}] Compaction: ${entry.tokensBefore} tokens summarized`);
      break;
    case "branch_summary":
      console.log(`[${entry.id}] Branch from ${entry.fromId}`);
      break;
    case "usage":
      console.log(`[${entry.id}] Usage (${entry.kind}): ${entry.usage.totalTokens} tokens`);
      break;
    case "custom":
      console.log(`[${entry.id}] Custom (${entry.customType}): ${JSON.stringify(entry.data)}`);
      break;
    case "custom_message":
      console.log(`[${entry.id}] Extension message (${entry.customType}): ${entry.content}`);
      break;
    case "label":
      console.log(`[${entry.id}] Label "${entry.label}" on ${entry.targetId}`);
      break;
    case "model_change":
      console.log(`[${entry.id}] Model: ${entry.provider}/${entry.modelId}`);
      break;
    case "thinking_level_change":
      console.log(`[${entry.id}] Thinking: ${entry.thinkingLevel}`);
      break;
  }
}
```


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/09-compaction.md -->
<!-- ============================================================ -->

# Compaction Reference

This reference describes automatic compaction, branch summarization, persisted entries, and extension hooks. For the user workflow, see [Sessions and Context](../02-run-pi/03-sessions.md#manage-conversation-context).

**Source files** ([pi](https://github.com/earendil-works/pi)):
- [`packages/coding-agent/src/core/compaction/compaction.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/compaction/compaction.ts) - Auto-compaction logic
- [`packages/coding-agent/src/core/compaction/branch-summarization.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts) - Branch summarization
- [`packages/coding-agent/src/core/compaction/utils.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/compaction/utils.ts) - Shared utilities (file tracking, serialization)
- [`packages/coding-agent/src/core/session-manager.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/session-manager.ts) - Entry types (`CompactionEntry`, `BranchSummaryEntry`)
- [`packages/coding-agent/src/core/extensions/types.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/extensions/types.ts) - Extension event types

For TypeScript definitions in your project, inspect `node_modules/@earendil-works/pi-coding-agent/dist/`.

## Overview

Pi has two summarization mechanisms:

| Mechanism | Trigger | Purpose |
|-----------|---------|---------|
| Compaction | Context exceeds threshold, or `/compact` | Summarize old messages to free up context |
| Branch summarization | `/tree` navigation | Preserve context when switching branches |

Both use closely related structured formats and track file operations cumulatively. Summarization requests disable prompt-cache writes because these one-off prompts are unlikely to be reused.

## Compaction

### When It Triggers

Auto-compaction triggers when:

```
contextTokens > contextWindow - reserveTokens
```

By default, `reserveTokens` is 16384 tokens (configurable in `~/.pi/agent/settings.json` or `<project-dir>/.pi/settings.json`). This leaves room for the LLM's response.

During a multi-turn agent run, Pi checks the canonical projected context after tools finish and their results are appended, before starting the next assistant response. If the threshold is crossed, Pi compacts during `prepareNextTurn`, then performs the existing catch-up steering poll before `turn_start`. It skips this between-turn check when the completed tool batch terminates the run and no queued message requires another response. Pi also checks before a new user prompt and performs final-attempt overflow recovery after the low-level run ends.

A provider context-overflow error or an early final `stopReason: "length"` can select one compact-and-retry recovery attempt. Length responses with tool calls retain their synthetic failed tool results and follow the ordinary tool/queue scheduler rather than forcing the run to end.

You can also trigger manually with `/compact [instructions]`, where optional instructions focus the summary.

### How It Works

1. **Find cut point**: Walk backwards through the finalized session projection, accumulating token estimates until `keepRecentTokens` (default 20k, configurable in `~/.pi/agent/settings.json` or `<project-dir>/.pi/settings.json`) is reached
2. **Extract messages**: Collect projected messages from the previous kept boundary (or session start) up to the cut point
3. **Generate summary**: Call LLM to summarize with structured format, passing the previous summary as iterative context when present
4. **Append entry**: Save `CompactionEntry` with summary and `firstKeptEntryId`
5. **Rebuilds context**: Session rebuilds the context for the next request, using summary + messages from `firstKeptEntryId` onwards

```
Before compaction:

  entry:  0     1     2     3      4     5     6      7      8     9
        ┌─────┬─────┬─────┬──────┬─────┬─────┬──────┬──────┬─────┬─────┐
        │ hdr │ usr │ ass │ tool │ usr │ ass │ tool │ tool │ ass │ tool│
        └─────┴─────┴─────┴──────┴─────┴─────┴──────┴──────┴─────┴─────┘
                └────────┬───────┘ └──────────────┬──────────────┘
               messagesToSummarize            kept messages
                                   ↑
                          firstKeptEntryId (entry 4)

After compaction (new entry appended):

  entry:  0     1     2     3      4     5     6      7      8     9     10
        ┌─────┬─────┬─────┬──────┬─────┬─────┬──────┬──────┬─────┬─────┬─────┐
        │ hdr │ usr │ ass │ tool │ usr │ ass │ tool │ tool │ ass │ tool│ cmp │
        └─────┴─────┴─────┴──────┴─────┴─────┴──────┴──────┴─────┴─────┴─────┘
               └──────────┬──────┘ └──────────────────────┬───────────────────┘
                 not sent to LLM                    sent to LLM
                                                         ↑
                                              starts from firstKeptEntryId

What the LLM sees:

  ┌────────┬─────────┬─────┬─────┬──────┬──────┬─────┬──────┐
  │ system │ summary │ usr │ ass │ tool │ tool │ ass │ tool │
  └────────┴─────────┴─────┴─────┴──────┴──────┴─────┴──────┘
       ↑         ↑      └─────────────────┬────────────────┘
    prompt   from cmp          messages from firstKeptEntryId
```

On repeated compactions, the summarized span starts at the previous compaction's kept boundary (`firstKeptEntryId`), not at the compaction entry itself, falling back to the entry after the previous compaction if that kept entry cannot be found in the path. A retain-none compaction records its own ID as `firstKeptEntryId`; repeated compaction starts after that entry. This preserves messages that survived the earlier compaction by including them in the next summarization pass as well. Pi also recalculates `tokensBefore` from the rebuilt, context-edited session projection before writing the new `CompactionEntry`, so the token count reflects the actual pre-compaction context being replaced. Omitted raw entries remain stored but do not affect cut selection, summaries, checkpoints, or token estimates.

### Overflow and Length Recovery Ordering

Recovery preserves the existing lifecycle and queue order. The completed attempt remains visible to `turn_end` and `agent_end`; post-run recovery then repairs persisted model context before a fresh retry:

```text
persist final assistant response
→ extension/public turn_end
→ extension/public agent_end
→ append context_edit omissions for the selected attempt
→ for overflow/length: run session_before_compact and append compaction on success
→ start the retry as a fresh run
```

If recovery compaction fails or is cancelled, Pi keeps the omission edits, appends no compaction, and schedules no internal retry. Existing queued work remains governed by ordinary steering and follow-up rules. `agent_before_settle` sees the repaired projection after recovery processing. Raw transcript history, exports, billing totals, and history-search extensions can still inspect the omitted attempt.

### Split user-message spans

A user-message span starts with a user message and includes all turns until the next user message. Normally, compaction cuts at user-message boundaries.

When one user-message span exceeds `keepRecentTokens`, the cut point lands within that span at an assistant message. This is a split user-message span:

```
Split user-message span (one span exceeds budget):

  entry:  0     1     2      3     4      5      6     7      8
        ┌─────┬─────┬─────┬──────┬─────┬──────┬──────┬─────┬──────┐
        │ hdr │ usr │ ass │ tool │ ass │ tool │ tool │ ass │ tool │
        └─────┴─────┴─────┴──────┴─────┴──────┴──────┴─────┴──────┘
                ↑                                     ↑
         turnStartIndex = 1                  firstKeptEntryId = 7
                │                                     │
                └──── turnPrefixMessages (1-6) ───────┘
                                                      └── kept (7-8)

  isSplitTurn = true
  messagesToSummarize = []  (no earlier user-message spans)
  turnPrefixMessages = [usr, ass, tool, ass, tool, tool]
```

For split user-message spans, Pi generates two summaries and merges them:
1. **History summary**: Previous context (if any)
2. **User-message-span prefix summary**: The early part of the split user-message span

### Cut Point Rules

Valid cut points are:
- User messages
- Assistant messages
- BashExecution messages
- Custom messages (custom_message, branch_summary)

Never cut at tool results (they must stay with their tool call).

Preparation advances the kept boundary into a context-invisible suffix only when that suffix contains an omitted assistant attempt and no unomitted context-producing entries. Recovery `context_edit` omissions satisfy this rule; intrinsically context-invisible metadata may coexist with them. Metadata alone and newly appended custom messages do not move the cut. A replacement edit affecting the candidate input or summarized prefix also blocks advancement because the omitted assistant answered the pre-edit input; replacements of suffix entries that are ultimately omitted remain safe. This allows an over-budget recovered input to be summarized while retaining the edits that keep the abandoned attempt omitted, without making bookkeeping change whether new model input is preserved verbatim.

### CompactionEntry Structure

Defined in [`session-manager.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/session-manager.ts):

```typescript
interface CompactionEntry<T = unknown> {
  type: "compaction";
  id: string;
  parentId: string | null;
  timestamp: string;
  summary: string;
  firstKeptEntryId: string;
  tokensBefore: number;
  usage?: Usage;       // LLM usage that generated the summary
  fromHook?: boolean;  // true if provided by extension (legacy field name)
  details?: T;         // implementation-specific data
}

// Default compaction uses this for details (from compaction.ts):
interface CompactionDetails {
  readFiles: string[];
  modifiedFiles: string[];
}
```

Extensions can store any JSON-serializable data in `details`. The default compaction tracks file operations, but custom extension implementations can use their own structure. Generated and extension-provided summaries store their LLM `usage` when available so session totals include summarization work.

See [`prepareCompaction()`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/compaction/compaction.ts) and [`compact()`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/compaction/compaction.ts) for the implementation. For direct programmatic summarization, `generateSummary()` returns the summary text and `generateSummaryWithUsage()` returns `{ text, usage }`.

## Branch Summarization

### When It Triggers

When you use `/tree` to navigate to a different branch, Pi offers to summarize the work you're leaving. This injects context from the left branch into the new branch.

### How It Works

1. **Find common ancestor**: Deepest node shared by old and new positions
2. **Collect entries**: Walk from old leaf back to common ancestor
3. **Prepare with budget**: Include messages up to token budget (newest first)
4. **Generate summary**: Call LLM with structured format
5. **Append entry**: Save `BranchSummaryEntry` at navigation point

```
Tree before navigation:

         ┌─ B ─ C ─ D (old leaf, being abandoned)
    A ───┤
         └─ E ─ F (target)

Common ancestor: A
Entries to summarize: B, C, D

After navigation with summary:

         ┌─ B ─ C ─ D
    A ───┤
         └─ E ─ F ─ [summary of B,C,D] (new leaf)
```

### Cumulative File Tracking

Default compaction and branch summarization track files cumulatively. Both extract file operations from tool calls in the messages being summarized. Compaction also carries file lists from the previous Pi-generated compaction. Branch summarization carries file lists from Pi-generated branch summaries in the entries it summarizes.

File tracking therefore accumulates across default compactions and nested default branch summaries. Pi does not automatically carry file lists from extension-generated summaries whose `fromHook` field is `true`; extensions manage their own `details` format.

### BranchSummaryEntry Structure

Defined in [`session-manager.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/session-manager.ts):

```typescript
interface BranchSummaryEntry<T = unknown> {
  type: "branch_summary";
  id: string;
  parentId: string | null;
  timestamp: string;
  summary: string;
  fromId: string;      // Entry we navigated from
  usage?: Usage;       // LLM usage that generated the summary
  fromHook?: boolean;  // true if provided by extension (legacy field name)
  details?: T;         // implementation-specific data
}

// Default branch summarization uses this for details (from branch-summarization.ts):
interface BranchSummaryDetails {
  readFiles: string[];
  modifiedFiles: string[];
}
```

Same as compaction, extensions can store custom data in `details`.

See [`collectEntriesForBranchSummary()`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts), [`prepareBranchEntries()`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts), and [`generateBranchSummary()`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts) for the implementation.

## Summary Format

Both formats include Goal, Constraints & Preferences, Progress, Key Decisions, and Next Steps. Compaction summaries also include Critical Context. Branch summaries stop after Next Steps. Pi appends file lists to either format when relevant.

Compaction summaries use this format:

```markdown
## Goal
[What the user is trying to accomplish]

## Constraints & Preferences
- [Requirements mentioned by user]

## Progress
### Done
- [x] [Completed tasks]

### In Progress
- [ ] [Current work]

### Blocked
- [Issues, if any]

## Key Decisions
- **[Decision]**: [Rationale]

## Next Steps
1. [What should happen next]

## Critical Context
- [Data needed to continue]

<read-files>
path/to/file1.ts
path/to/file2.ts
</read-files>

<modified-files>
path/to/changed.ts
</modified-files>
```

### Message Serialization

Before summarization, messages are serialized to text via [`serializeConversation()`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/compaction/utils.ts):

```
[User]: What they said
[Assistant thinking]: Internal reasoning
[Assistant]: Response text
[Assistant tool calls]: read(path="foo.ts"); edit(path="bar.ts", ...)
[Tool result]: Output from tool
```

This prevents the model from treating it as a conversation to continue.

Tool results are truncated to 2000 characters during serialization. Content beyond that limit is replaced with a marker indicating how many characters were truncated. This keeps summarization requests within reasonable token budgets, since tool results (especially from `read` and `bash`) are typically the largest contributors to context size.

## Custom Summarization via Extensions

Extensions can intercept and customize both compaction and branch summarization. See [`extensions/types.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/extensions/types.ts) for event type definitions.

### session_before_compact

Fired before auto-compaction or `/compact`. Can cancel or provide custom summary. See `SessionBeforeCompactEvent` and `CompactionPreparation` in the types file.

```typescript
pi.on("session_before_compact", async (event, ctx) => {
  const { preparation, branchEntries, customInstructions, reason, willRetry, signal } = event;

  // preparation.messagesToSummarize - messages to summarize
  // preparation.turnPrefixMessages - user-message-span prefix (if isSplitTurn)
  // preparation.previousSummary - previous compaction summary
  // preparation.fileOps - extracted file operations
  // preparation.tokensBefore - context tokens before compaction
  // preparation.firstKeptEntryId - where kept messages start
  // preparation.settings - effective settings after applying model overrides

  // branchEntries - all entries on current branch (for custom state)
  // reason - "manual" (/compact), "threshold", or "overflow"
  // willRetry - whether the aborted turn is retried after compaction (overflow recovery)
  // signal - AbortSignal (pass to LLM calls)

  // Cancel:
  return { cancel: true };

  // Custom summary:
  return {
    compaction: {
      summary: "Your summary...",
      firstKeptEntryId: preparation.firstKeptEntryId,
      tokensBefore: preparation.tokensBefore,
      // usage: summaryResponse.usage, // Optional; included in session totals
      details: { /* custom data */ },
    }
  };
});
```

#### Converting Messages to Text

To generate a summary with your own model, convert messages to text using `serializeConversation`:

```typescript
import { convertToLlm, serializeConversation } from "@earendil-works/pi-coding-agent";

pi.on("session_before_compact", async (event, ctx) => {
  const { preparation } = event;
  
  // Convert AgentMessage[] to Message[], then serialize to text
  const conversationText = serializeConversation(
    convertToLlm(preparation.messagesToSummarize)
  );
  // Returns:
  // [User]: message text
  // [Assistant thinking]: thinking content
  // [Assistant]: response text
  // [Assistant tool calls]: read(path="..."); bash(command="...")
  // [Tool result]: output text

  // Now send to your model for summarization
  const { summary, usage } = await myModel.summarize(conversationText);
  
  return {
    compaction: {
      summary,
      firstKeptEntryId: preparation.firstKeptEntryId,
      tokensBefore: preparation.tokensBefore,
      usage,
    }
  };
});
```

See [custom-compaction.ts](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/custom-compaction.ts) for a complete example using a different model.

### session_compact_failed

Fired when manual or automatic compaction fails or is aborted. This is useful for telemetry extensions that need to pair `session_before_compact` attempts with terminal outcomes.

```typescript
pi.on("session_compact_failed", async (event, ctx) => {
  const { reason, errorMessage, aborted, willRetry, fromExtension } = event;
  // reason - "manual" (/compact), "threshold", or "overflow"
  // errorMessage - present for non-abort failures
  // aborted - true for canceled/aborted compactions
  // willRetry - whether the aborted turn would have retried after compaction
  // fromExtension - whether extension-provided compaction content was being used
});
```

### session_before_tree

Fired before `/tree` navigation. Always fires regardless of whether user chose to summarize. Can cancel navigation or provide custom summary.

```typescript
pi.on("session_before_tree", async (event, ctx) => {
  const { preparation, signal } = event;

  // preparation.targetId - where we're navigating to
  // preparation.oldLeafId - current position (being abandoned)
  // preparation.commonAncestorId - shared ancestor
  // preparation.entriesToSummarize - entries that would be summarized
  // preparation.userWantsSummary - whether user chose to summarize

  // Cancel navigation entirely:
  return { cancel: true };

  // Provide custom summary (only used if userWantsSummary is true):
  if (preparation.userWantsSummary) {
    return {
      summary: {
        summary: "Your summary...",
        // usage: summaryResponse.usage, // Optional; included in session totals
        details: { /* custom data */ },
      }
    };
  }
});
```

See `SessionBeforeTreeEvent` and `TreePreparation` in the types file.

## Settings

Configure compaction in `~/.pi/agent/settings.json` or `<project-dir>/.pi/settings.json`:

```json
{
  "compaction": {
    "enabled": true,
    "reserveTokens": 16384,
    "keepRecentTokens": 20000
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enable auto-compaction |
| `reserveTokens` | `16384` | Tokens to reserve for LLM response |
| `keepRecentTokens` | `20000` | Recent tokens to keep (not summarized) |

Disable auto-compaction with `"enabled": false`. You can still compact manually with `/compact`.

### Per-model overrides

Use `compaction.modelOverrides` to tune token budgets for different models:

```json
{
  "compaction": {
    "reserveTokens": 16384,
    "keepRecentTokens": 20000,
    "modelOverrides": {
      "some-provider/big-model": {
        "reserveTokens": 400000
      }
    }
  }
}
```

For a model with a 1M context window, this override triggers compaction above 600K tokens and keeps the ordinary 20000 recent tokens. Other models retain the ordinary 16384-token reserve. `reserveTokens` also influences summarization output limits, capped by the model's maximum output tokens; it is not solely a trigger threshold.

Keys are exact, case-sensitive `provider/modelId` values, including any slashes within the model ID. Each `reserveTokens` and `keepRecentTokens` value falls back independently from the model override to the ordinary setting to the built-in default. Values must be non-negative safe integers. Invalid values in the matching model override produce an error when read; only omitted fields fall back to the ordinary setting. Model override entries must be objects. Invalid ordinary token settings produce an error when read, even if the active model has a valid override. Only omitted ordinary values use built-in defaults. `enabled` remains global, not model-specific.

These resolved values are used for manual compaction, all automatic threshold checks, overflow recovery, and extension-visible `preparation.settings`. Model switches affect subsequent checks and compactions without changing ordinary settings. Compaction already in progress uses the model and settings captured for that operation. Branch summarization settings are unaffected.

Overrides work in both global and project settings. The files merge recursively before lookup, so a global model-specific value beats a project-wide fallback; a project must override that model entry to change it. See [Settings](../05-reference/04-settings.md#per-model-compaction-overrides) for details.


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/10-json.md -->
<!-- ============================================================ -->

# JSON Event Stream

JSON mode emits structured progress for one invocation:

```bash
pi --mode json "Review this repository"
```

Pi writes one session header followed by session events, then exits after the supplied prompts finish. RPC mode emits the same session-event shapes but has no session header because it is a bidirectional, long-lived protocol. See [RPC Mode](../05-reference/11-rpc.md).

This page is the canonical reference for events shared by JSON and RPC mode. Message values use the [shared message types](../05-reference/14-message-types.md).

## Framing and process I/O

The stream uses strict JSONL framing. Each record is one JSON object terminated by LF (`\n`). Split records only on LF and strip an optional preceding carriage return. Unicode line and paragraph separators are valid inside JSON strings and are not record boundaries.

Node.js `readline` is not suitable for this stream because it also recognizes those Unicode separators. Use a byte or UTF-8 stream decoder and split on LF.

Read stdout continuously. A reader that stops consuming records can stall Pi when the pipe buffer fills. Stdout is reserved for JSONL; diagnostics and application logging go to stderr.

## Session header

The first JSON-mode record is the current [session header](../05-reference/08-session-format.md#sessionheader):

```json
{"type":"session","version":3,"id":"uuid","timestamp":"2024-12-03T14:00:00.000Z","cwd":"/path"}
```

RPC mode does not emit this record. Use [`get_state`](../05-reference/12-rpc-commands.md#get_state) for its current session ID and file.

## Event sequence

A basic run produces records like these:

```json
{"type":"agent_start"}
{"type":"turn_start"}
{"type":"message_start","message":{"role":"user","content":"Review this repository","timestamp":1733234401000}}
{"type":"message_end","message":{"role":"user","content":"Review this repository","timestamp":1733234401000}}
{"type":"message_start","message":{"role":"assistant","content":[],"stopReason":"pending","...":"..."}}
{"type":"message_update","usage":{"...":"..."},"assistantMessageEvent":{"type":"text_delta","contentIndex":0,"delta":"Hello"}}
{"type":"message_end","message":{"role":"assistant","...":"..."}}
{"type":"turn_end","message":{"role":"assistant","...":"..."},"toolResults":[]}
{"type":"agent_end","messages":[{"...":"..."}],"willRetry":false}
{"type":"agent_settled"}
```

`agent_end` closes one low-level agent run. Automatic retry, overflow recovery, compaction retry, steering, or follow-up work can still continue. `agent_settled` means Pi has no remaining automatic work for that session-level run.

## Agent and turn events

| Event | Fields | Meaning |
|---|---|---|
| `agent_start` | None | A low-level agent run started. |
| `agent_end` | `messages`, `willRetry` | That low-level run ended. `messages` contains messages generated by the run. |
| `agent_settled` | None | Pi will not continue automatically through retries, compaction recovery, or queued messages. |
| `turn_start` | None | One assistant turn started. |
| `turn_end` | `message`, `toolResults` | One assistant response and its resulting tool calls finished. |

A turn is one assistant response plus any tool calls and tool results produced by that response.

## Message events

| Event | Fields | Meaning |
|---|---|---|
| `message_start` | `message` | A message started. |
| `message_update` | `usage`, `assistantMessageEvent` | An assistant message emitted a content-block update. |
| `message_end` | `message` | A message completed. This is the authoritative final message. |

### Reconstruct streaming messages

Wire `message_update` records are delta-only. They omit the SDK event's cumulative `message` field and every `assistantMessageEvent.partial` snapshot so stream size remains linear.

The nested event is one of:

| Type | Fields in addition to `type` | Meaning |
|---|---|---|
| `start` | None | The provider stream started; its cumulative `partial` field is removed on the wire. |
| `text_start` | `contentIndex` | A text block started. |
| `text_delta` | `contentIndex`, `delta` | Append text to the block. |
| `text_end` | `contentIndex`, `content` | The text block ended with authoritative content. |
| `thinking_start` | `contentIndex` | A thinking block started. |
| `thinking_delta` | `contentIndex`, `delta` | Append thinking text to the block. |
| `thinking_end` | `contentIndex`, `content` | The thinking block ended with authoritative content. |
| `toolcall_start` | `contentIndex`, `id`, `toolName` | A tool-call block started. |
| `toolcall_delta` | `contentIndex`, `delta` | Append serialized argument data. |
| `toolcall_end` | `contentIndex`, `toolCall` | The tool call ended with the complete `ToolCall`. |
| `done` | `reason`, `message` | The provider stream completed successfully. |
| `error` | `reason`, `error` | The provider stream ended with an error or abort message. |

The normal agent loop translates provider-level `start`, `done`, and `error` into `message_start` and `message_end` session events rather than emitting them as `message_update`. They remain admitted by the exported `JsonAgentSessionEvent` transformation for callers that construct a matching session event.

Use `contentIndex` to identify the content block. Buffer `delta` fields for a live display, but replace reconstructed data with the completed content in `text_end`, `thinking_end`, or `toolcall_end`. Replace the whole partial message with `message_end.message` when it arrives.

The top-level `usage` is the latest cumulative provider-reported usage for the assistant response. It can remain zero until completion when a provider does not report usage while streaming.

```json
{"type":"message_update","usage":{"input":100,"output":1,"cacheRead":0,"cacheWrite":0,"totalTokens":101,"cost":{"input":0,"output":0,"cacheRead":0,"cacheWrite":0,"total":0}},"assistantMessageEvent":{"type":"text_delta","contentIndex":0,"delta":"Hello "}}
```

## Tool execution events

| Event | Fields | Meaning |
|---|---|---|
| `tool_execution_start` | `toolCallId`, `toolName`, `args` | Tool execution started. |
| `tool_execution_update` | `toolCallId`, `toolName`, `args`, `partialResult` | The tool reported a partial result. |
| `tool_execution_end` | `toolCallId`, `toolName`, `result`, `isError` | Tool execution finished. |

Use `toolCallId` to correlate the lifecycle. `partialResult` is the latest partial result supplied by the tool. Whether it replaces or extends an earlier update depends on that tool's result contract.

```json
{"type":"tool_execution_start","toolCallId":"call_abc123","toolName":"bash","args":{"command":"ls -la"}}
{"type":"tool_execution_update","toolCallId":"call_abc123","toolName":"bash","args":{"command":"ls -la"},"partialResult":{"content":[{"type":"text","text":"partial output"}],"details":{}}}
{"type":"tool_execution_end","toolCallId":"call_abc123","toolName":"bash","result":{"content":[{"type":"text","text":"complete output"}],"details":{}},"isError":false}
```

## Queue and state events

| Event | Fields | Meaning |
|---|---|---|
| `queue_update` | `steering`, `followUp` | The pending steering or follow-up queue changed. Both fields contain the complete current queue. |
| `entry_appended` | `entry` | An extension appended a custom session entry through `pi.appendEntry()`. |
| `session_info_changed` | `name` | The session display name changed. An absent `name` means it was cleared. |
| `thinking_level_changed` | `level` | The active thinking level changed. |

The `entry` value uses a persisted [session entry type](../05-reference/08-session-format.md#entry-types).

## Compaction events

`compaction_start` reports why compaction began:

```json
{"type":"compaction_start","reason":"threshold"}
```

`reason` is `"manual"`, `"threshold"`, or `"overflow"`.

`compaction_end` contains the result when compaction succeeds:

```json
{
  "type": "compaction_end",
  "reason": "threshold",
  "result": {
    "summary": "Summary of conversation...",
    "firstKeptEntryId": "abc123",
    "tokensBefore": 150000,
    "estimatedTokensAfter": 32000,
    "usage": {"...": "..."},
    "details": {}
  },
  "aborted": false,
  "willRetry": false
}
```

If compaction was aborted, `result` is absent and `aborted` is true. If it failed, `result` is absent, `aborted` is false, and `errorMessage` describes the failure. Successful overflow recovery sets `willRetry` to true before Pi retries the prompt.

See [Compaction and Branch Summaries](../05-reference/09-compaction.md) for result semantics.

## Retry events

Assistant-turn retry emits:

```json
{"type":"auto_retry_start","attempt":1,"maxAttempts":3,"delayMs":2000,"errorMessage":"529 overloaded"}
{"type":"auto_retry_end","success":true,"attempt":2}
```

On final failure, `auto_retry_end` has `success: false` and a `finalError` string.

Compaction and branch-summary retry emit:

```json
{"type":"summarization_retry_scheduled","attempt":1,"maxAttempts":3,"delayMs":2000,"errorMessage":"terminated"}
{"type":"summarization_retry_attempt_start","source":"compaction","reason":"threshold"}
{"type":"summarization_retry_finished"}
```

For a branch summary, `source` is `"branchSummary"` and `reason` is absent. The `reason` on a compaction retry is `"manual"`, `"threshold"`, or `"overflow"`.

## RPC-only events

A direct RPC [`bash`](../05-reference/12-rpc-commands.md#bash) command emits one `bash_execution_update` for each output chunk. Its optional `id` matches the command ID. The final command response can contain truncated output, but these events stream all output:

```json
{"type":"bash_execution_update","id":"req-1","delta":"total 48\n"}
```

RPC also adds `extension_error` when an extension handler throws:

```json
{"type":"extension_error","extensionPath":"/path/to/extension.ts","event":"tool_call","error":"Error message"}
```

Extension UI records are a separate RPC subprotocol, not `AgentSessionEvent` values. See [RPC Extension UI](../05-reference/13-rpc-extension-ui.md).

## TypeScript types

The SDK's `AgentSessionEvent` contains cumulative streaming snapshots for in-process consumers. JSON and RPC transform only `message_update`:

```typescript
type WithoutPartial<T> = T extends { partial: unknown } ? Omit<T, "partial"> : T;

type JsonAssistantMessageEvent<T> = T extends { type: "toolcall_start"; partial: unknown }
  ? WithoutPartial<T> & { id: string; toolName: string }
  : WithoutPartial<T>;

type JsonAgentSessionEvent =
  | Exclude<AgentSessionEvent, { type: "message_update" }>
  | {
      type: "message_update";
      usage: Usage;
      assistantMessageEvent: JsonAssistantMessageEvent<AssistantMessageEvent>;
    };
```

Use the exported `JsonAgentSessionEvent` type from `@earendil-works/pi-coding-agent`. Its implementation is in [`json-event.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/modes/json-event.ts).

## Example

Print completed messages from a one-shot run:

```bash
pi --mode json "List files" 2>/dev/null | jq -c 'select(.type == "message_end")'
```


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/11-rpc.md -->
<!-- ============================================================ -->

# RPC Mode

RPC mode runs Pi as a long-lived subprocess controlled through JSON records on stdin and stdout. Use it for language-independent integrations, process isolation, IDEs, and custom user interfaces.

For an in-process Node.js or Bun integration, prefer the [SDK](../04-build-on-pi/06-sdk.md). For a subprocess-based TypeScript integration, prefer the exported `RpcClient`, which starts Pi, correlates responses, exposes typed command methods, and delivers events to listeners.

| Interface | Process boundary | Control model | Best fit |
|---|---|---|---|
| [SDK](../04-build-on-pi/06-sdk.md) | In process | Direct TypeScript methods and events | Node.js or Bun hosts that want complete API access |
| RPC | Child process | JSONL commands, responses, and events | Other languages, isolated processes, IDEs, or custom clients |

## Start RPC mode

```bash
pi --mode rpc --no-session
```

Normal CLI options still select the working folder, model, tools, resources, and session behavior. Common choices include `--provider`, `--model`, `--name`, `--no-session`, and `--session-dir`. See [Command Line](../05-reference/01-cli.md) for the complete, version-specific interface; `pi --help` is authoritative for the installed version.

RPC mode rejects `@file` prompt arguments. Send prompts through the [`prompt`](../05-reference/12-rpc-commands.md#prompt) command instead.

## Protocol records

The protocol has four record families:

| Direction | Record | Purpose |
|---|---|---|
| stdin | Command | Ask Pi to prompt, inspect state, change configuration, or manage the session |
| stdout | `response` | Report whether one command succeeded and return any command data |
| stdout | Session event | Stream run, message, tool, queue, compaction, and retry activity |
| Both | Extension UI record | Forward supported extension interactions between Pi and the client |

See [RPC Commands](../05-reference/12-rpc-commands.md), [JSON Event Stream](../05-reference/10-json.md), and [RPC Extension UI](../05-reference/13-rpc-extension-ui.md) for the canonical record definitions.

### Correlate commands and responses

Every command accepts an optional string `id`. A matching response repeats it:

```json
{"id":"req-1","type":"get_state"}
{"id":"req-1","type":"response","command":"get_state","success":true,"data":{"...":"..."}}
```

Use unique IDs whenever more than one command can be outstanding. Command handling is asynchronous, so clients should correlate by ID rather than response order.

Session events generally have no command ID because they describe session activity. `bash_execution_update` is the exception: when the originating [`bash`](../05-reference/12-rpc-commands.md#bash) command has an ID, its output events repeat that ID.

An `extension_ui_response` uses the ID supplied by its `extension_ui_request`. It does not produce a normal command response.

## Framing

RPC uses strict JSONL framing. Write one complete JSON object per record and terminate it with LF (`\n`). Read stdout as a byte or UTF-8 stream and split records only on LF. Strip an optional preceding carriage return to accept CRLF input.

Do not use a generic line reader that treats Unicode line or paragraph separators as record boundaries. In particular, Node.js `readline` also splits on `U+2028` and `U+2029`, which are valid inside JSON strings.

Read stdout continuously. Pi honors stdout backpressure, but a client that stops reading can stall the process. Honor stdin backpressure when writing commands. Stdout is reserved for protocol records; diagnostics and application logging go to stderr.

## Run lifecycle

A successful `prompt` response means the prompt was accepted, queued, or handled. It does not mean model work completed:

```json
{"id":"req-2","type":"prompt","message":"Review this repository"}
{"id":"req-2","type":"response","command":"prompt","success":true,"data":{"disposition":"started"}}
```

`data.disposition` reports what happened to the prompt. If it is `"handled"`, no run started for this prompt, so don't wait for `agent_settled`. See [RPC Commands](../05-reference/12-rpc-commands.md#prompt) for all values.

Continue consuming [events](../05-reference/10-json.md) after that response. `agent_end` marks the end of one low-level agent run, but retries, overflow recovery, compaction, steering, or follow-up work can still follow. Wait for `agent_settled` when the client needs to know Pi will not continue automatically.

Subscribe before sending a prompt to avoid missing a fast completion. `RpcClient.promptAndWait()` does this internally. If using separate `RpcClient` calls, install the event listener before `prompt()` and call `waitForIdle()` only while a run is active.

## Errors

A failed command returns one response with `success: false`:

```json
{"id":"req-3","type":"response","command":"set_model","success":false,"error":"Model not found: invalid/model"}
```

Malformed JSON produces a parse response without a request ID:

```json
{"type":"response","command":"parse","success":false,"error":"Failed to parse command: Unexpected token..."}
```

A success response only covers command handling. Provider failures and aborts after a prompt is accepted appear in the message and event stream.

Clients must also handle child-process startup failures, unexpected exits, stderr diagnostics, cancellation, and their own deadlines. Do not parse stderr as protocol data.

## Shutdown

Close the child's stdin to request an orderly shutdown. Pi disposes the active runtime before exiting. Clients should still handle process signals and unexpected exits.

An extension can also request shutdown through its extension context. Pi completes shutdown after the current command or after the active run emits `agent_settled`.

## Minimal client

This Python example uses a binary pipe reader, which splits on LF without treating Unicode separators as protocol boundaries:

```python
import json
import subprocess

process = subprocess.Popen(
    ["pi", "--mode", "rpc", "--no-session"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

assert process.stdin is not None
assert process.stdout is not None

command = {"id": "prompt-1", "type": "prompt", "message": "Hello"}
process.stdin.write(json.dumps(command).encode("utf-8") + b"\n")
process.stdin.flush()

while line := process.stdout.readline():
    record = json.loads(line)
    if record.get("type") == "message_update":
        update = record["assistantMessageEvent"]
        if update["type"] == "text_delta":
            print(update["delta"], end="", flush=True)
    elif record.get("type") == "agent_settled":
        print()
        break

process.stdin.close()
process.wait()
```

For maintained TypeScript clients, use the checked [RPC client example](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/rpc-client.ts). It requires a built Pi CLI because the repository example points to `dist/cli.js`.

## Reference

- [RPC Commands](../05-reference/12-rpc-commands.md): every stdin command and response
- [JSON Event Stream](../05-reference/10-json.md): shared stdout session events and streaming reconstruction
- [RPC Extension UI](../05-reference/13-rpc-extension-ui.md): dialogs, notifications, responses, and limitations
- [Message Types](../05-reference/14-message-types.md): messages and content blocks used by responses and events
- [Session File Format](../05-reference/08-session-format.md): entries returned by session commands
- [`rpc-types.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/modes/rpc/rpc-types.ts): exported TypeScript protocol definitions
- [`RpcClient`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/modes/rpc/rpc-client.ts): subprocess client implementation

## Moved reference anchors

The detailed references formerly on this page now have dedicated pages. These anchors preserve existing links.

<a id="prompt"></a>
<a id="steer"></a>
<a id="follow_up"></a>
<a id="abort"></a>
<a id="clear_queue"></a>
<a id="new_session"></a>
<a id="get_state"></a>
<a id="get_messages"></a>
<a id="set_model"></a>
<a id="cycle_model"></a>
<a id="get_available_models"></a>
<a id="set_thinking_level"></a>
<a id="cycle_thinking_level"></a>
<a id="get_available_thinking_levels"></a>
<a id="set_steering_mode"></a>
<a id="set_follow_up_mode"></a>
<a id="compact"></a>
<a id="set_auto_compaction"></a>
<a id="set_auto_retry"></a>
<a id="abort_retry"></a>
<a id="bash"></a>
<a id="abort_bash"></a>
<a id="get_session_stats"></a>
<a id="export_html"></a>
<a id="switch_session"></a>
<a id="fork"></a>
<a id="clone"></a>
<a id="get_fork_messages"></a>
<a id="get_entries"></a>
<a id="get_tree"></a>
<a id="get_last_assistant_text"></a>
<a id="set_session_name"></a>
<a id="get_commands"></a>

Command details moved to [RPC Commands](../05-reference/12-rpc-commands.md).

<a id="message_update-streaming"></a>
<a id="bash_execution_update"></a>
<a id="compaction_start--compaction_end"></a>
<a id="summarization_retry_scheduled--summarization_retry_attempt_start--summarization_retry_finished"></a>

Event details moved to [JSON Event Stream](../05-reference/10-json.md).

<a id="extension-ui-protocol"></a>

Extension interaction details moved to [RPC Extension UI](../05-reference/13-rpc-extension-ui.md).


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/12-rpc-commands.md -->
<!-- ============================================================ -->

# RPC Commands

This reference lists commands accepted on stdin in [RPC mode](../05-reference/11-rpc.md). Each command and response is one JSON object. Shared message values use the [message types](../05-reference/14-message-types.md).

## Prompting

### prompt

Send a user prompt to the agent. The command response is emitted after the prompt is accepted, queued, or handled. Events continue streaming asynchronously after acceptance.

```json
{"id": "req-1", "type": "prompt", "message": "Hello, world!"}
```

With images:
```json
{"type": "prompt", "message": "What's in this image?", "images": [{"type": "image", "data": "base64-encoded-data", "mimeType": "image/png"}]}
```

**During streaming**: If the agent is already streaming, you must specify `streamingBehavior` to queue the message:

```json
{"type": "prompt", "message": "New instruction", "streamingBehavior": "steer"}
```

- `"steer"`: Queue the message while the agent is running. It is delivered after the current assistant turn finishes executing its tool calls, before the next LLM call.
- `"followUp"`: Wait until the agent finishes. Message is delivered only when agent stops.

If the agent is streaming and no `streamingBehavior` is specified, the command returns an error.

**Extension commands**: If the message is an extension command (e.g., `/mycommand`), it executes immediately even during streaming. Extension commands manage their own LLM interaction via `pi.sendMessage()`.

**Input expansion**: Skill commands (`/skill:name`) and prompt templates (`/template`) are expanded before sending/queueing.

Response:
```json
{"id": "req-1", "type": "response", "command": "prompt", "success": true, "data": {"disposition": "started"}}
```

`data.disposition` is `"handled"` if an extension command or input handler consumed the prompt, `"queued"` if Pi queued it during a run, or `"started"` if Pi accepted it to start a run. This describes the submitted prompt, not independent work started by an extension or a guarantee of completion.

`success: true` means the prompt was accepted, queued, or handled immediately. `success: false` means the prompt was rejected before acceptance. Failures after acceptance are reported through the normal event and message stream, not as a second `response` for the same request id.

The `images` field is optional. Each image uses `ImageContent` format: `{"type": "image", "data": "base64-encoded-data", "mimeType": "image/png"}`.

### steer

Queue a steering message while the agent is running. It is delivered after the current assistant turn finishes executing its tool calls, before the next LLM call. Skill commands and prompt templates are expanded. Extension commands are not allowed (use `prompt` instead).

```json
{"type": "steer", "message": "Stop and do this instead"}
```

With images:
```json
{"type": "steer", "message": "Look at this instead", "images": [{"type": "image", "data": "base64-encoded-data", "mimeType": "image/png"}]}
```

The `images` field is optional. Each image uses `ImageContent` format (same as `prompt`).

Response:
```json
{"type": "response", "command": "steer", "success": true, "data": {"disposition": "queued"}}
```

`data.disposition` is `"handled"` if an input handler consumed this steer, or `"queued"` if Pi queued it (including after a handler transformed it). It does not guarantee this message remains queued.

See [set_steering_mode](#set_steering_mode) for controlling how steering messages are processed.

### follow_up

Queue a follow-up message to be processed after the agent finishes. Delivered only when agent has no more tool calls or steering messages. Skill commands and prompt templates are expanded. Extension commands are not allowed (use `prompt` instead).

```json
{"type": "follow_up", "message": "After you're done, also do this"}
```

With images:
```json
{"type": "follow_up", "message": "Also check this image", "images": [{"type": "image", "data": "base64-encoded-data", "mimeType": "image/png"}]}
```

The `images` field is optional. Each image uses `ImageContent` format (same as `prompt`).

Response:
```json
{"type": "response", "command": "follow_up", "success": true, "data": {"disposition": "queued"}}
```

`data.disposition` has the same `"handled"` or `"queued"` meaning as for `steer`, applied to this follow-up.

See [set_follow_up_mode](#set_follow_up_mode) for controlling how follow-up messages are processed.

### abort

Abort the current operation and wait for the session to become idle before responding.

```json
{"type": "abort"}
```

Response:
```json
{"type": "response", "command": "abort", "success": true}
```

### clear_queue

Remove queued steering and follow-up messages and return their text.

```json
{"type": "clear_queue"}
```

Response:
```json
{
  "type": "response",
  "command": "clear_queue",
  "success": true,
  "data": {
    "steering": ["Change direction"],
    "followUp": ["Summarize when finished"]
  }
}
```

To implement interactive Esc behavior, send `clear_queue` before `abort`, then restore the returned text in the client editor. `abort` continues queued messages when they remain in the session.

### new_session

Start a fresh session. Can be canceled by a `session_before_switch` extension event handler.

```json
{"type": "new_session"}
```

With optional parent session tracking:
```json
{"type": "new_session", "parentSession": "/path/to/parent-session.jsonl"}
```

Response:
```json
{"type": "response", "command": "new_session", "success": true, "data": {"cancelled": false}}
```

If an extension canceled:
```json
{"type": "response", "command": "new_session", "success": true, "data": {"cancelled": true}}
```

## State

### get_state

Get current session state.

```json
{"type": "get_state"}
```

Response:
```json
{
  "type": "response",
  "command": "get_state",
  "success": true,
  "data": {
    "model": {...},
    "thinkingLevel": "medium",
    "isStreaming": false,
    "isCompacting": false,
    "steeringMode": "all",
    "followUpMode": "one-at-a-time",
    "sessionFile": "/path/to/session.jsonl",
    "sessionId": "abc123",
    "sessionName": "my-feature-work",
    "autoCompactionEnabled": true,
    "messageCount": 5,
    "pendingMessageCount": 0
  }
}
```

The `model` field is a full [Model](#model-object) object, or omitted when no model is selected. The `sessionName` field is the display name set via `set_session_name`, or omitted if not set.

### get_messages

Get all messages in the conversation.

```json
{"type": "get_messages"}
```

Response:
```json
{
  "type": "response",
  "command": "get_messages",
  "success": true,
  "data": {"messages": [...]}
}
```

Messages are `AgentMessage` objects (see [Message Types](../05-reference/14-message-types.md)).

## Model

### set_model

Switch to a specific model.

```json
{"type": "set_model", "provider": "anthropic", "modelId": "claude-sonnet-4-20250514"}
```

Response contains the full [Model](#model-object) object:
```json
{
  "type": "response",
  "command": "set_model",
  "success": true,
  "data": {...}
}
```

### cycle_model

Cycle to the next available model. Returns `null` data if only one model available.

```json
{"type": "cycle_model"}
```

Response:
```json
{
  "type": "response",
  "command": "cycle_model",
  "success": true,
  "data": {
    "model": {...},
    "thinkingLevel": "medium",
    "isScoped": false
  }
}
```

The `model` field is a full [Model](#model-object) object.

### get_available_models

List all configured models.

```json
{"type": "get_available_models"}
```

Response contains an array of full [Model](#model-object) objects:
```json
{
  "type": "response",
  "command": "get_available_models",
  "success": true,
  "data": {
    "models": [...]
  }
}
```

## Thinking

### set_thinking_level

Set the reasoning/thinking level for models that support it.

```json
{"type": "set_thinking_level", "level": "high"}
```

Levels: `"off"`, `"minimal"`, `"low"`, `"medium"`, `"high"`, `"xhigh"`, `"max"`

`"xhigh"` and `"max"` are exposed only when supported by the selected model. Some models, including GPT-5.6, expose both.

Response:
```json
{"type": "response", "command": "set_thinking_level", "success": true}
```

### cycle_thinking_level

Cycle through available thinking levels. Returns `null` data if model doesn't support thinking.

```json
{"type": "cycle_thinking_level"}
```

Response:
```json
{
  "type": "response",
  "command": "cycle_thinking_level",
  "success": true,
  "data": {"level": "high"}
}
```

### get_available_thinking_levels

List the thinking levels supported by the current model. Returns `["off"]` for a model without reasoning support.

```json
{"type": "get_available_thinking_levels"}
```

Response:
```json
{
  "type": "response",
  "command": "get_available_thinking_levels",
  "success": true,
  "data": {
    "levels": ["off", "minimal", "low", "medium", "high"]
  }
}
```

## Queue modes

### set_steering_mode

Control how steering messages (from `steer`) are delivered.

```json
{"type": "set_steering_mode", "mode": "one-at-a-time"}
```

Modes:
- `"all"`: Deliver all steering messages after the current assistant turn finishes executing its tool calls
- `"one-at-a-time"`: Deliver one steering message per completed assistant turn (default)

Response:
```json
{"type": "response", "command": "set_steering_mode", "success": true}
```

### set_follow_up_mode

Control how follow-up messages (from `follow_up`) are delivered.

```json
{"type": "set_follow_up_mode", "mode": "one-at-a-time"}
```

Modes:
- `"all"`: Deliver all follow-up messages when agent finishes
- `"one-at-a-time"`: Deliver one follow-up message per agent completion (default)

Response:
```json
{"type": "response", "command": "set_follow_up_mode", "success": true}
```

## Compaction

### compact

Manually compact conversation context to reduce token usage.

```json
{"type": "compact"}
```

With custom instructions:
```json
{"type": "compact", "customInstructions": "Focus on code changes"}
```

Response:
```json
{
  "type": "response",
  "command": "compact",
  "success": true,
  "data": {
    "summary": "Summary of conversation...",
    "firstKeptEntryId": "abc123",
    "tokensBefore": 150000,
    "estimatedTokensAfter": 32000,
    "usage": {
      "input": 32000,
      "output": 1200,
      "cacheRead": 0,
      "cacheWrite": 0,
      "totalTokens": 33200,
      "cost": {"input": 0.01, "output": 0.02, "cacheRead": 0, "cacheWrite": 0, "total": 0.03}
    },
    "details": {}
  }
}
```

`estimatedTokensAfter` is a heuristic estimate over the rebuilt message context immediately after compaction, not a provider-exact token count. `usage` reports the LLM call or calls that generated the summary and may be omitted by custom compaction handlers.

### set_auto_compaction

Enable or disable automatic compaction when context is nearly full.

```json
{"type": "set_auto_compaction", "enabled": true}
```

Response:
```json
{"type": "response", "command": "set_auto_compaction", "success": true}
```

## Retry

### set_auto_retry

Enable or disable automatic retry on transient errors (overloaded, rate limit, 5xx).

```json
{"type": "set_auto_retry", "enabled": true}
```

Response:
```json
{"type": "response", "command": "set_auto_retry", "success": true}
```

### abort_retry

Abort an in-progress retry (cancel the delay and stop retrying).

```json
{"type": "abort_retry"}
```

Response:
```json
{"type": "response", "command": "abort_retry", "success": true}
```

## Bash

### bash

Execute a shell command and add output to conversation context. Output streams as `bash_execution_update` events while the command runs; the response contains the final result.

```json
{"id": "req-1", "type": "bash", "command": "ls -la"}
```

Set `excludeFromContext` to `true` when the command output should be stored in the session but omitted from the model context on the next prompt.

Include an `id` to associate streamed `bash_execution_update` events with this command.

Response:
```json
{
  "id": "req-1",
  "type": "response",
  "command": "bash",
  "success": true,
  "data": {
    "output": "total 48\ndrwxr-xr-x ...",
    "exitCode": 0,
    "cancelled": false,
    "truncated": false
  }
}
```

If output was truncated, includes `fullOutputPath`:
```json
{
  "type": "response",
  "command": "bash",
  "success": true,
  "data": {
    "output": "truncated output...",
    "exitCode": 0,
    "cancelled": false,
    "truncated": true,
    "fullOutputPath": "/tmp/pi-bash-abc123.log"
  }
}
```

**How bash results reach the LLM:**

The `bash` command executes immediately and returns a `BashResult`. Internally, a `BashExecutionMessage` is created and stored in the agent's message state.

When the next `prompt` command is sent, Pi transforms context messages before sending them to the model. Unless `excludeFromContext` is true, the `BashExecutionMessage` becomes a `UserMessage` with this format:

````
Ran `ls -la`
```
total 48
drwxr-xr-x ...
```
````

This means:
1. Included bash output reaches the model on the **next prompt**, not immediately.
2. Multiple bash commands can run before a prompt; Pi includes each output that does not set `excludeFromContext`.

### abort_bash

Abort a running bash command.

```json
{"type": "abort_bash"}
```

Response:
```json
{"type": "response", "command": "abort_bash", "success": true}
```

## Session

### get_session_stats

Get token usage, cost statistics, and current context window usage.

```json
{"type": "get_session_stats"}
```

Response:
```json
{
  "type": "response",
  "command": "get_session_stats",
  "success": true,
  "data": {
    "sessionFile": "/path/to/session.jsonl",
    "sessionId": "abc123",
    "userMessages": 5,
    "assistantMessages": 5,
    "toolCalls": 12,
    "toolResults": 12,
    "totalMessages": 22,
    "tokens": {
      "input": 50000,
      "output": 10000,
      "cacheRead": 40000,
      "cacheWrite": 5000,
      "total": 105000
    },
    "cost": 0.45,
    "contextUsage": {
      "tokens": 60000,
      "contextWindow": 200000,
      "percent": 30
    }
  }
}
```

`tokens` and `cost` include assistant messages, usage reported by tools, and compaction/branch-summary generation across the full session. `contextUsage` contains the actual current context-window estimate used for compaction and footer display.

`contextUsage` is omitted when no model or context window is available. `contextUsage.tokens` and `contextUsage.percent` are `null` immediately after compaction until a fresh post-compaction assistant response provides valid usage data.

### export_html

Export session to an HTML file.

```json
{"type": "export_html"}
```

With custom path:
```json
{"type": "export_html", "outputPath": "/tmp/session.html"}
```

Response:
```json
{
  "type": "response",
  "command": "export_html",
  "success": true,
  "data": {"path": "/tmp/session.html"}
}
```

### switch_session

Load a different session file. Can be canceled by a `session_before_switch` extension event handler.

```json
{"type": "switch_session", "sessionPath": "/path/to/session.jsonl"}
```

Response:
```json
{"type": "response", "command": "switch_session", "success": true, "data": {"cancelled": false}}
```

If an extension canceled the switch:
```json
{"type": "response", "command": "switch_session", "success": true, "data": {"cancelled": true}}
```

### fork

Create a new fork from a previous user message on the active branch. Can be canceled by a `session_before_fork` extension event handler. Returns the text of the message being forked from.

```json
{"type": "fork", "entryId": "abc123"}
```

Response:
```json
{
  "type": "response",
  "command": "fork",
  "success": true,
  "data": {"text": "The original prompt text...", "cancelled": false}
}
```

If an extension canceled the fork:
```json
{
  "type": "response",
  "command": "fork",
  "success": true,
  "data": {"cancelled": true}
}
```

### clone

Duplicate the current active branch into a new session at the current position. Can be canceled by a `session_before_fork` extension event handler.

```json
{"type": "clone"}
```

Response:
```json
{
  "type": "response",
  "command": "clone",
  "success": true,
  "data": {"cancelled": false}
}
```

If an extension canceled the clone:
```json
{
  "type": "response",
  "command": "clone",
  "success": true,
  "data": {"cancelled": true}
}
```

### get_fork_messages

Get user messages available for forking.

```json
{"type": "get_fork_messages"}
```

Response:
```json
{
  "type": "response",
  "command": "get_fork_messages",
  "success": true,
  "data": {
    "messages": [
      {"entryId": "abc123", "text": "First prompt..."},
      {"entryId": "def456", "text": "Second prompt..."}
    ]
  }
}
```

### get_entries

Get all session entries in append order (excluding the session header). The session is an append-only tree of entries with stable ids, so an entry id works as a durable cursor: pass the last entry id you have seen as `since` to get only entries strictly after it, even across client restarts. Unlike `get_messages`, this includes pre-compaction history and abandoned branches.

```json
{"type": "get_entries"}
```

With a cursor:
```json
{"type": "get_entries", "since": "abc123"}
```

Response:
```json
{
  "type": "response",
  "command": "get_entries",
  "success": true,
  "data": {
    "entries": [
      {"type": "message", "id": "def456", "parentId": "abc123", "timestamp": "...", "message": {"role": "user", "...": "..."}}
    ],
    "leafId": "def456"
  }
}
```

`leafId` is the id of the current leaf entry (`null` for an empty session), so a client can tell in one round trip whether the active branch moved. If `since` does not match any entry id, the response is `success: false`.

### get_tree

Get the session as a tree of entries. Each node is `{entry, children, label?, labelTimestamp?}`. The result is an array because navigation APIs can create multiple roots; orphaned entries with broken parent chains also appear as roots.

```json
{"type": "get_tree"}
```

Response:
```json
{
  "type": "response",
  "command": "get_tree",
  "success": true,
  "data": {
    "tree": [
      {
        "entry": {"type": "message", "id": "abc123", "parentId": null, "...": "..."},
        "children": [
          {"entry": {"type": "message", "id": "def456", "parentId": "abc123", "...": "..."}, "children": []}
        ]
      }
    ],
    "leafId": "def456"
  }
}
```

### get_last_assistant_text

Get the text content of the last assistant message.

```json
{"type": "get_last_assistant_text"}
```

Response:
```json
{
  "type": "response",
  "command": "get_last_assistant_text",
  "success": true,
  "data": {"text": "The assistant's response..."}
}
```

The `text` value is `null` if no assistant text exists.

### set_session_name

Set a display name for the current session. The name appears in session listings and helps identify sessions.

```json
{"type": "set_session_name", "name": "my-feature-work"}
```

Response:
```json
{
  "type": "response",
  "command": "set_session_name",
  "success": true
}
```

The current session name is available via `get_state` in the `sessionName` field. To set the initial name when starting RPC mode, pass `--name <name>` or `-n <name>` to the `pi --mode rpc` process.

## Discoverable commands

### get_commands

Get available commands (extension commands, prompt templates, and skills). Run one through the `prompt` command by prefixing its name with `/`.

```json
{"type": "get_commands"}
```

Response:
```json
{
  "type": "response",
  "command": "get_commands",
  "success": true,
  "data": {
    "commands": [
      {
        "name": "fix-tests",
        "description": "Fix failing tests",
        "source": "prompt",
        "sourceInfo": {
          "path": "/home/user/myproject/.pi/agent/prompts/fix-tests.md",
          "source": "local",
          "scope": "project",
          "origin": "top-level"
        }
      }
    ]
  }
}
```

Each command has:
- `name`: Command name (use `/name`)
- `description`: Human-readable description (optional for extension commands)
- `source`: What kind of command:
  - `"extension"`: Registered via `pi.registerCommand()` in an extension
  - `"prompt"`: Loaded from a prompt template `.md` file
  - `"skill"`: Loaded from a skill directory (name is prefixed with `skill:`)
- `sourceInfo`: Metadata for the resource that registered the command:
  - `path`: Absolute path to the resource
  - `source`: How Pi discovered it, such as `"local"`, `"auto"`, or `"cli"`
  - `scope`: `"user"`, `"project"`, or `"temporary"`
  - `origin`: `"top-level"` for a directly loaded resource or `"package"` for a package resource
  - `baseDir`: Package base directory, when applicable

**Note**: Built-in TUI commands (`/settings`, `/hotkeys`, etc.) are not included. They are handled only in interactive mode and would not execute if sent via `prompt`.

## Model object

Model commands return the complete configured model definition. Costs are in US dollars per million tokens.

```json
{
  "id": "claude-sonnet-4-20250514",
  "name": "Claude Sonnet 4",
  "api": "anthropic-messages",
  "provider": "anthropic",
  "baseUrl": "https://api.anthropic.com",
  "reasoning": true,
  "input": ["text", "image"],
  "contextWindow": 200000,
  "maxTokens": 16384,
  "cost": {
    "input": 3.0,
    "output": 15.0,
    "cacheRead": 0.3,
    "cacheWrite": 3.75
  }
}
```

For model configuration, see [Configure a compatible endpoint](../02-run-pi/02-models.md#configure-a-compatible-endpoint). For TypeScript, use the exported `Model` type from `@earendil-works/pi-ai`.


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/13-rpc-extension-ui.md -->
<!-- ============================================================ -->

# RPC Extension UI

Extensions can request user interaction through `ctx.ui`. In RPC mode, supported calls become a request/response subprotocol alongside normal [RPC commands](../05-reference/12-rpc-commands.md) and [session events](../05-reference/10-json.md).

There are two categories of extension UI methods:

- **Dialog methods** (`select`, `confirm`, `input`, `editor`): emit an `extension_ui_request` on stdout and block until the client sends back an `extension_ui_response` on stdin with the matching `id`.
- **Fire-and-forget methods** (`notify`, `setStatus`, `setWidget`, `setTitle`, `set_editor_text`): emit an `extension_ui_request` on stdout but do not expect a response. The client can display the information or ignore it.

If a dialog method includes a `timeout` field, the agent-side will auto-resolve with a default value when the timeout expires. The client does not need to track timeouts.

## Limitations

Some `ExtensionUIContext` methods are not supported or degraded in RPC mode because they require direct terminal UI access:

- `custom()` returns `undefined`.
- `onTerminalInput()` returns a no-op unsubscribe function.
- `setWorkingMessage()`, `setWorkingVisible()`, `setWorkingIndicator()`, `setHiddenThinkingLabel()`, `setFooter()`, `setHeader()`, `addAutocompleteProvider()`, `setEditorComponent()`, and `setToolsExpanded()` are no-ops.
- `getEditorText()` returns `""` and `getEditorComponent()` returns `undefined`.
- `getToolsExpanded()` returns `false`.
- `pasteToEditor()` delegates to `setEditorText()` without terminal paste handling.
- `getAllThemes()` returns `[]`, and `getTheme()` returns `undefined`.
- `setTheme()` returns `{ success: false, error: "Theme switching not supported in RPC mode" }`.

Note: `ctx.mode` is `"rpc"` and `ctx.hasUI` is `true` in RPC mode because the dialog and fire-and-forget methods are functional via the extension UI sub-protocol. Use `ctx.mode === "tui"` to guard TUI-specific features like `custom()` that require a real terminal.

## Requests from Pi

All requests have `type: "extension_ui_request"`, a unique `id`, and a `method` field.

### select

Prompt the user to choose from a list. Dialog methods with a `timeout` field include the timeout in milliseconds; the agent auto-resolves with `undefined` if the client doesn't respond in time.

```json
{
  "type": "extension_ui_request",
  "id": "uuid-1",
  "method": "select",
  "title": "Allow dangerous command?",
  "options": ["Allow", "Block"],
  "timeout": 10000
}
```

Expected response: `extension_ui_response` with `value` (the selected option string) or `cancelled: true`.

### confirm

Prompt the user for yes/no confirmation.

```json
{
  "type": "extension_ui_request",
  "id": "uuid-2",
  "method": "confirm",
  "title": "Clear session?",
  "message": "All messages will be lost.",
  "timeout": 5000
}
```

Expected response: `extension_ui_response` with `confirmed: true/false` or `cancelled: true`.

### input

Prompt the user for free-form text.

```json
{
  "type": "extension_ui_request",
  "id": "uuid-3",
  "method": "input",
  "title": "Enter a value",
  "placeholder": "type something..."
}
```

Expected response: `extension_ui_response` with `value` (the entered text) or `cancelled: true`.

### editor

Open a multi-line text editor with optional prefilled content.

```json
{
  "type": "extension_ui_request",
  "id": "uuid-4",
  "method": "editor",
  "title": "Edit some text",
  "prefill": "Line 1\nLine 2\nLine 3"
}
```

Expected response: `extension_ui_response` with `value` (the edited text) or `cancelled: true`.

### notify

Display a notification. Fire-and-forget, no response expected.

```json
{
  "type": "extension_ui_request",
  "id": "uuid-5",
  "method": "notify",
  "message": "Command blocked by user",
  "notifyType": "warning"
}
```

The `notifyType` field is `"info"`, `"warning"`, or `"error"`. Defaults to `"info"` if omitted.

### setStatus

Set or clear a status entry in the footer/status bar. Fire-and-forget.

```json
{
  "type": "extension_ui_request",
  "id": "uuid-6",
  "method": "setStatus",
  "statusKey": "my-ext",
  "statusText": "Turn 3 running..."
}
```

Send `statusText: undefined` (or omit it) to clear the status entry for that key.

### setWidget

Set or clear a widget (block of text lines) displayed above or below the editor. Fire-and-forget.

```json
{
  "type": "extension_ui_request",
  "id": "uuid-7",
  "method": "setWidget",
  "widgetKey": "my-ext",
  "widgetLines": ["--- My Widget ---", "Line 1", "Line 2"],
  "widgetPlacement": "aboveEditor"
}
```

Send `widgetLines: undefined` (or omit it) to clear the widget. The `widgetPlacement` field is `"aboveEditor"` (default) or `"belowEditor"`. Only string arrays are supported in RPC mode; component factories are ignored.

### setTitle

Set the terminal window/tab title. Fire-and-forget.

```json
{
  "type": "extension_ui_request",
  "id": "uuid-8",
  "method": "setTitle",
  "title": "pi - my project"
}
```

### set_editor_text

Set the text in the input editor. Fire-and-forget.

```json
{
  "type": "extension_ui_request",
  "id": "uuid-9",
  "method": "set_editor_text",
  "text": "prefilled text for the user"
}
```

## Responses to Pi

Responses are sent for dialog methods only (`select`, `confirm`, `input`, `editor`). The `id` must match the request.

### Value response (select, input, editor)

```json
{"type": "extension_ui_response", "id": "uuid-1", "value": "Allow"}
```

### Confirmation response (confirm)

```json
{"type": "extension_ui_response", "id": "uuid-2", "confirmed": true}
```

### Cancellation response (any dialog)

Dismiss any dialog method. The extension receives `undefined` (for select/input/editor) or `false` (for confirm).

```json
{"type": "extension_ui_response", "id": "uuid-3", "cancelled": true}
```

## Example

See the checked [RPC extension UI client](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/rpc-extension-ui.ts) and its [demo extension](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/rpc-demo.ts).

The exported request and response unions are defined in [`rpc-types.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/modes/rpc/rpc-types.ts). See [Extensions](../04-build-on-pi/01-extensions.md#ui-and-modes) for mode-independent extension guidance.


<!-- ============================================================ -->
<!-- SOURCE: 05-reference/14-message-types.md -->
<!-- ============================================================ -->

# Message Types

Pi uses `AgentMessage` values in SDK state, lifecycle events, RPC responses, and persisted session message entries. This page defines those shared messages and their content blocks.

Message timestamps are Unix timestamps in milliseconds. They are different from the ISO 8601 timestamps on [session entries](../05-reference/08-session-format.md#entry-base).

Source definitions:

- [`packages/ai/src/types.ts`](https://github.com/earendil-works/pi/blob/main/packages/ai/src/types.ts) defines provider-facing messages and content blocks.
- [`packages/agent/src/types.ts`](https://github.com/earendil-works/pi/blob/main/packages/agent/src/types.ts) defines the extensible `AgentMessage` union.
- [`packages/coding-agent/src/core/messages.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/messages.ts) adds coding-agent message roles.

## Content blocks

### TextContent

```typescript
interface TextContent {
  type: "text";
  text: string;
  textSignature?: string;
}
```

`textSignature` contains provider-specific message metadata. Treat it as opaque.

### ImageContent

```typescript
interface ImageContent {
  type: "image";
  data: string;
  mimeType: string;
}
```

`data` is base64-encoded image data. `mimeType` identifies its media type, such as `image/png` or `image/jpeg`.

### ThinkingContent

```typescript
interface ThinkingContent {
  type: "thinking";
  thinking: string;
  thinkingSignature?: string;
  redacted?: boolean;
}
```

Thinking signatures contain provider-specific replay data. Treat them as opaque. A redacted block can have no visible thinking text while retaining an encrypted payload in `thinkingSignature`.

### ToolCall

```typescript
interface ToolCall {
  type: "toolCall";
  id: string;
  name: string;
  arguments: Record<string, any>;
  thoughtSignature?: string;
  namespace?: string;
}
```

`thoughtSignature` is provider-specific. `namespace` identifies an OpenAI Responses namespace for dynamically loaded or namespaced tools.

## Usage

Assistant messages always contain usage. Tool results can contain usage when the tool performed nested model work.

```typescript
interface Usage {
  input: number;
  output: number;
  cacheRead: number;
  cacheWrite: number;
  cacheWrite1h?: number;
  reasoning?: number;
  totalTokens: number;
  cost: {
    input: number;
    output: number;
    cacheRead: number;
    cacheWrite: number;
    total: number;
  };
}
```

When present, `reasoning` is already included in `output`; do not add it again. `cacheWrite1h` is the subset of `cacheWrite` written with one-hour retention.

## Base messages

### SystemMessage

```typescript
interface SystemMessage {
  role: "system";
  content: string | TextContent[];
  sections?: Record<string, string | null>;
  toolsAdded?: Tool[];
  toolsRemoved?: ToolReference[];
  replace?: boolean;
  timestamp: number;
}
```

The leading system message declares the initial prompt and tools. Later system messages can append instructions, replace or remove named prompt sections, and add or remove tools. Replaying them in order yields the current state. A message with `replace: true` discards the earlier state and establishes a complete new baseline.

### UserMessage

```typescript
interface UserMessage {
  role: "user";
  content: string | (TextContent | ImageContent)[];
  timestamp: number;
}
```

### AssistantMessage

```typescript
interface AssistantMessage {
  role: "assistant";
  content: (TextContent | ThinkingContent | ToolCall)[];
  api: string;
  provider: string;
  model: string;
  responseModel?: string;
  responseId?: string;
  providerThinkingLevel?: string;
  diagnostics?: AssistantMessageDiagnostic[];
  usage: Usage;
  stopReason: "pending" | "stop" | "length" | "toolUse" | "error" | "aborted" | "deferred";
  deferred?: DeferredHandle;
  errorMessage?: string;
  rawStopReason?: string;
  endTurn?: boolean;
  timestamp: number;
}
```

`responseModel` records a concrete provider response model when it differs from the requested model. `responseId`, `providerThinkingLevel`, `diagnostics`, and `rawStopReason` preserve provider or runtime details.

`"pending"` is used for a partial assistant message while it streams. The completed message in `message_end` has a terminal stop reason, and Pi does not persist `"pending"` assistant messages in session JSONL.

A `"deferred"` response has a `DeferredHandle` with the provider data needed to retrieve it:

```typescript
interface DeferredHandle {
  provider: string;
  modelId: string;
  api: string;
  id: string;
  expiresAt?: number;
  pollAfterMs?: number;
  data?: JsonValue;
}
```

### ToolResultMessage

```typescript
interface ToolResultMessage<TDetails = any> {
  role: "toolResult";
  toolCallId: string;
  toolName: string;
  content: (TextContent | ImageContent)[];
  details?: TDetails;
  usage?: Usage;
  isError: boolean;
  timestamp: number;
}
```

`details` is tool-specific. Optional `usage` reports nested model work performed by the tool and contributes to full-session statistics, but it is not part of the main model-call usage.

## Coding-agent messages

The coding-agent package extends `AgentMessage` with four roles.

### BashExecutionMessage

Created by direct shell commands, including the RPC [`bash`](../05-reference/12-rpc-commands.md#bash) command. It is not an LLM tool result.

```typescript
interface BashExecutionMessage {
  role: "bashExecution";
  command: string;
  output: string;
  exitCode: number | undefined;
  cancelled: boolean;
  truncated: boolean;
  fullOutputPath?: string;
  excludeFromContext?: boolean;
  timestamp: number;
}
```

Unless `excludeFromContext` is true, Pi converts this message to user-role text before the next model request.

### CustomMessage

Created when an extension sends a context message.

```typescript
interface CustomMessage<T = unknown> {
  role: "custom";
  customType: string;
  content: string | (TextContent | ImageContent)[];
  display: boolean;
  details?: T;
  timestamp: number;
}
```

Pi converts its content to a user message for model requests. `display` controls terminal rendering; `details` is not sent to the model.

### BranchSummaryMessage

```typescript
interface BranchSummaryMessage {
  role: "branchSummary";
  summary: string;
  fromId: string | null;
  timestamp: number;
}
```

Pi creates this context message from a persisted `branch_summary` entry.

### CompactionSummaryMessage

```typescript
interface CompactionSummaryMessage {
  role: "compactionSummary";
  summary: string;
  tokensBefore: number;
  timestamp: number;
}
```

Pi creates this context message from a persisted `compaction` entry.

## AgentMessage union

In the coding agent, the union is equivalent to:

```typescript
type AgentMessage =
  | SystemMessage
  | UserMessage
  | AssistantMessage
  | ToolResultMessage
  | BashExecutionMessage
  | CustomMessage
  | BranchSummaryMessage
  | CompactionSummaryMessage;
```

At the lower-level agent package, `AgentMessage` is `Message | CustomAgentMessages[keyof CustomAgentMessages]`. Applications can add roles through TypeScript declaration merging, so consumers should tolerate unknown custom roles when they accept messages from an augmented host.
