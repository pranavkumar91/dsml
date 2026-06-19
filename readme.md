# DSML — Dialogue State Markup Language

DSML is a minimal XML-based framework for building conversational applications.

Instead of writing rigid chatbot flows with hardcoded asks, replies, buttons, and intents, DSML describes only the **available conversational options** and the **required data** for each option.

The language model handles the rest: asking natural questions, extracting user inputs, routing between options, remembering context, and switching between linked XML files.

## Core Idea

Traditional chatbot frameworks usually require:

```text
intents
utterances
ask tags
say tags
choice tags
button flows
hardcoded responses
```

DSML avoids this.

A DSML file can be as simple as:

```xml
<dsml>
  <option name="home" />

  <option name="about" />

  <option name="menu" />

  <option name="table_booking">
    <required name="name" />
    <required name="phone" />
    <required name="time" />
    <required name="people" />
  </option>
</dsml>
```

The XML does not script what the bot says.

It only says:

```text
what states exist
what data each state requires
```

The LLM generates the conversation dynamically.

## Philosophy

DSML does not script conversation.

DSML defines conversational affordances.

The runtime reads the XML, checks the current option, finds missing required fields, asks the LLM to generate a natural request, takes user input, extracts values, updates memory, and routes to the next option.

In short:

```text
XML = structure
LLM = conversational renderer
memory = continuity
runtime = loop
```

## Runtime Loop

The basic DSML runtime loop looks like this:

```text
start at current option
↓
read required fields
↓
check memory for missing values
↓
LLM generates a natural question/request
↓
user replies
↓
LLM extracts structured values
↓
memory updates
↓
if all required fields are complete, LLM routes to next option
↓
switch option or linked XML file
```

## Example Conversation

Given this DSML:

```xml
<option name="table_booking">
  <required name="name" />
  <required name="phone" />
  <required name="time" />
  <required name="people" />
</option>
```

The runtime may produce:

```text
BOT: Sure, I can help you book a table. What name, time, and number of people should I use?
USER: Amit, 8 pm, 4 people.

BOT: Great. Can you share your phone number?
USER: 9876543210.
```

The XML never defined those exact questions. It only defined the required fields.

## Linked XML Files

DSML supports modular conversational documents.

Example:

```xml
<dsml>
  <option name="home" />
  <option name="booking" src="booking.xml#home" />
  <option name="support" src="support.xml#home" />
</dsml>
```

This allows reusable modules such as:

```text
booking.xml
payment.xml
support.xml
restaurant_menu.xml
hotel_room_query.xml
salon_appointment.xml
```

When the runtime enters an option with a `src`, it loads the linked XML file and switches to the target option.

Memory continues across file switches.

## Minimal Tags

Current tentative DSML spec:

### `<dsml>`

Root element of a DSML file.

```xml
<dsml>
  ...
</dsml>
```

### `<option>`

Defines a conversational state.

```xml
<option name="home" />
```

An option may also link to another XML file:

```xml
<option name="booking" src="booking.xml#home" />
```

### `<required>`

Declares a required data field inside an option.

```xml
<option name="table_booking">
  <required name="name" />
  <required name="phone" />
  <required name="time" />
  <required name="people" />
</option>
```

## What DSML Does Not Need

DSML currently avoids:

```text
<intent>
<ask>
<say>
<choice>
<request>
<button>
```

The LLM is responsible for language generation and routing.

The XML remains declarative and minimal.

## Example Project Structure

```text
dsml/
  main.py
  runtime.py
  main.xml
  booking.xml
  .env
  README.md
```

## Example `.env`

```env
GOOGLE_API_KEY=your_google_api_key_here
```

## Installation

```bash
pip install python-dotenv
pip install langchain langchain-core langchain-google-genai
```

## Basic Usage

```python
from runtime import DSMLRuntime

bot = DSMLRuntime("main.xml", session_id="user_123")
bot.run()
```

## Memory

DSML uses two kinds of memory:

### 1. Slot Memory

Structured values extracted from the user:

```python
{
  "name": "Amit",
  "time": "8 pm",
  "people": "4",
  "phone": "9876543210"
}
```

### 2. Conversation Memory

The full chat history managed through LangChain.

This lets the bot remember earlier conversation even after switching XML files.

## Why DSML?

DSML is useful because the same XML can power many interfaces:

```text
CLI bot
WhatsApp bot
Telegram bot
website chatbot
voice bot
hotel kiosk
local business assistant
```

The transport changes, but the DSML file remains the same.

## Possible Use Cases

```text
restaurant table booking
hotel room enquiry
salon appointments
local business catalogues
customer support
lead capture
service booking
quiz flows
AI forms
conversational websites
```

## Design Goal

The goal of DSML is to make conversational apps feel like documents.

Instead of designing rigid chatbot trees, we define semantic states and required data.

The runtime and LLM convert that structure into a live conversation.

## Status

This project is experimental.

Current focus:

```text
minimal XML spec
CLI runtime
LangChain integration
memory support
linked XML switching
LLM-based asking
LLM-based extraction
LLM-based routing
```

Future possibilities:

```text
web renderer
WhatsApp renderer
Telegram renderer
visual DSML editor
component registry
hosted DSML modules
validation rules
tool calling
business templates
```

## Working Principle

DSML is based on one simple idea:

```text
Do not write the conversation.
Define the conversational document.
```

The model can speak.

The XML should only define what exists and what is needed.
