# QuickGPT
Access Chat GPT directly from the terminal.
- Focused on, and will default to providing short answers for simple questions
### Roadmap
In rough order of targeted completion
- API call to chatGPT 
- Inline call from terminal with no flags returning answer limited to ~50 words
- Terminal arguments to allow adjusted output parameters
    - E.g. -v verbose (unlimited length) return
    - Pre tuned context prompts e.g. "Do not explain"
- Installer that compiles python script as a binary and adds it to environment, allowing it to be called from anywhere in the system
- Take text files as input, or output
- Allow expanded/ continous interaction, either through successive inline terminal calls or in an interative mode, to allow contigous conversations
- Take code files as input context, and answer prompt questions
    - define a function of an input code file to be specifically analysed, instead of the whole file to improve performance (may not be neccesary)
    - Use a prompt to generate a function or other code snippet that is appended to a code file
        - Provide a preview of code snippet before appending
