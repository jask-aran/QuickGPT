# QuickGPT
Access Chat GPT directly from the terminal.
- Focused on, and will default to providing short answers for simple questions
### Roadmap
In rough order of targeted completion

~~API call to chatGPT~~

~~Inline call from terminal with no flags returning answer limited to around 50 words~~
~~Allow for successive inline calls from terminal to continue a conversation, allowing for answers between other work in the terminal. This requires storing conversation history between script executions, probably in JSON~~ 

This was removed, it is uneccessary to have a successive conversation over multiple terminal calls, as continued conversations generally benefit from long input and output lengths, which would significantly clutter the terminal and be hard to read. Instead extra functionality has been added to the conversational mode to allow saving of messages and dumping of whole message history to txt and json files respectively.
- Terminal arguments to allow adjusted output parameters
    - E.g. -v verbose (unlimited length) return
    - Pre tuned context prompts e.g. "Do not explain"
- Installer that compiles python script as a binary and adds it to environment, allowing it to be called from anywhere in the system
- Take text files as input, or output

- Take code files as input context, and answer prompt questions
    - define a function of an input code file to be specifically analysed, instead of the whole file to improve performance (may not be neccesary)
    - Use a prompt to generate a function or other code snippet that is appended to a code file
        - Provide a preview of code snippet before appending

- Integrate with Windows PowerToys Run, to allow for quick searches directly from a floating (called with win + space) search bar

### Completed
- API calls to GPT-3.5-Turbo, the model powering chatGPT are made with input prompts and a system context statement that commands the model to give concise answers that are limited to 50 words, which are returned to the terminal.
- Added both an inline terminal mode, and a conversational mode that is not restricted t0 50 word responses in a continous conversational mode.