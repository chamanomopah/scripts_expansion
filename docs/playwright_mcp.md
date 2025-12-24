Playwright MCP (Model Context Protocol) is a server that enables AI agents, such as Large Language Models (LLMs) or chat assistants, to interact with web pages using Playwright's browser automation capabilities. It provides a structured way for these agents to understand and manipulate web elements, bypassing the need for visual interpretation through screenshots or visually-tuned models.
Key features and tools offered by Playwright MCP:
Browser Automation: It allows AI agents to perform actions in a real browser environment, including navigation, clicking elements, filling forms, and more.
Structured Accessibility Snapshots: Instead of relying on visual information, Playwright MCP provides AI agents with structured data about the page's accessibility tree, including roles, labels, and attributes, facilitating more robust and stable interactions.
JavaScript Execution: Agents can execute JavaScript code within the browser context, enabling dynamic interactions and data manipulation.
Screenshot Capabilities: While focusing on structured data, it still offers the ability to capture screenshots for debugging or visual verification.
Console Log Monitoring: Allows for monitoring and capturing console logs during browser interactions, aiding in debugging and analysis.
Integration with AI Clients: Designed to be used with various AI clients, including chat assistants, editor plugins, and Node.js scripts, acting as a bridge between the AI and Playwright's browser control.
Multi-Browser Support: Leverages Playwright's ability to automate across different browser engines like Chromium, Firefox, and WebKit.
API Testing Capabilities: Can be used to validate API endpoints and ensure the reliability of web applications.
How it works:
The Playwright MCP server acts as an intermediary. AI agents send requests to the MCP server describing desired browser actions in a human-understandable format. The server then translates these requests into Playwright commands, executes them in the browser, and returns the resulting state or information back to the AI agent. This abstraction simplifies browser interaction for AI models, allowing them to focus on understanding user intent rather than the intricacies of browser automation APIs.


Available tools
With the MCP loaded you can run /mcp and then navigate to playwright to view all available tools. Here's the full list:

browser_close (read-only)
browser_resize (read-only)
browser_console_messages (read-only)
browser_handle_dialog
browser_file_upload
browser_install
browser_press_key
browser_navigate
browser_navigate_back (read-only)
browser_navigate_forward (read-only)
browser_network_requests (read-only)
browser_pdf_save (read-only)
browser_take_screenshot (read-only)
browser_snapshot (read-only)
browser_click
browser_drag
browser_hover (read-only)
browser_type
browser_select_option
browser_tab_list (read-only)
browser_tab_new (read-only)
browser_tab_select (read-only)
browser_tab_close
browser_generate_playwright_test (read-only)
browser_wait_for (read-only)
You don't have to reference these by name, Claude should usually be smart enough to pick the right one for the task at hand.