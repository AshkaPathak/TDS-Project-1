# TDS Project 1 — Q4: CommonMark Markdown Parser

## Problem Summary

Implement a **CommonMark-compatible Markdown parser** in Python.

The function must be:

```python
def parse_markdown(markdown):
```

and should convert Markdown text into the correct **HTML output** according to the CommonMark specification.

### Constraints

The implementation must:

- Use **pure Python**
- Only use the **standard library**
- **No external packages**
- **No subprocess calls**
- **No network access**
- Work inside the **Pyodide execution environment**

The parser is evaluated using **CommonMark specification tests**, which check if the produced HTML exactly matches expected output.

---

# Core Idea

Markdown parsing is implemented in two stages:

1. **Block Parsing**
2. **Inline Parsing**

This mirrors the structure of the **CommonMark parsing model**.

```
Markdown
   ↓
Block parser
   ↓
Block AST
   ↓
Inline parser
   ↓
HTML renderer
```

---

# Stage 1 — Block Parsing

The block parser processes the Markdown **line-by-line** and builds a tree of block nodes.

### Supported Block Types

The implementation supports:

- Paragraphs
- ATX headings (`#`)
- Setext headings
- Thematic breaks (`---`)
- Fenced code blocks
- Indented code blocks
- Blockquotes (`>`)
- Ordered lists
- Unordered lists
- HTML blocks

Each detected block becomes a **Node** object.

Example structure:

```
Document
 ├─ Heading
 ├─ Paragraph
 └─ List
     ├─ ListItem
     └─ ListItem
```

---

# Stage 2 — Inline Parsing

After block structure is built, inline syntax is parsed inside paragraphs.

Supported inline elements:

- emphasis (`*italic*`)
- strong (`**bold**`)
- code spans (`` `code` ``)
- inline links
- reference links
- images

Example transformation:

```
Markdown:
This is *important* text

HTML:
<p>This is <em>important</em> text</p>
```

---

# Handling Emphasis

CommonMark emphasis rules require **delimiter matching logic** rather than simple regex replacement.

The implementation:

1. Scans the text
2. Builds a delimiter stack
3. Matches opening and closing runs of `*` or `_`
4. Produces `<em>` or `<strong>` tags accordingly.

---

# Handling Lists

List detection is based on:

```
- item
+ item
* item
1. item
2) item
```

The parser tracks:

- marker indentation
- content column
- continuation lines

Example:

```
- one
- two
```

Parsed as:

```html
<ul>
<li>one</li>
<li>two</li>
</ul>
```

### Tight vs Loose Lists

A list item containing only a single paragraph is rendered as a **tight list**:

```
<li>text</li>
```

rather than:

```
<li><p>text</p></li>
```

This is implemented by detecting single-paragraph list items during rendering.

---

# Reference Link Definitions

Reference links are extracted before block parsing.

Example:

```
[example]: https://example.com
```

Stored internally as:

```
refs[label] = (url, title)
```

This allows links like:

```
[example]
```

to be resolved later during inline parsing.

---

# HTML Block Handling

The parser recognizes HTML blocks including:

- `<pre>`
- `<script>`
- `<style>`
- comments
- CDATA sections
- block-level HTML tags

These blocks are passed directly to the output without modification.

---

# Code Spans

Backtick runs are handled carefully to follow CommonMark rules.

Example:

```
`code`
```

becomes

```html
<code>code</code>
```

Whitespace normalization inside code spans is also implemented.

---

# Rendering

After parsing, nodes are converted to HTML using a renderer.

Examples:

### Paragraph

```
<p>text</p>
```

### Heading

```
<h1>Title</h1>
```

### List

```
<ul>
<li>item</li>
</ul>
```

### Code Block

```
<pre><code>...</code></pre>
```

---

# Final Implementation

The final function returns HTML with a trailing newline to match CommonMark test expectations.

```python
def parse_markdown(markdown):
    # Implementation provided in solution.py
```

The parser successfully passes the CommonMark specification tests used by the assignment.

---

# Conclusion

This implementation demonstrates a simplified **CommonMark-style Markdown parser** built entirely with the Python standard library.

Key techniques used:

- block-level parsing
- delimiter stack for emphasis
- reference link extraction
- structured AST representation
- HTML rendering phase

The final solution correctly handles the Markdown features required by the evaluation tests and produces HTML compliant with the expected specification output.


