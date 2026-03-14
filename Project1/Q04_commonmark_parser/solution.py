def parse_markdown(markdown):
    import re
    import html
    import string

    def escape_html(s):
        return html.escape(s, quote=False)

    def normalize_label(label):
        return " ".join(label.strip().split()).casefold()

    def detab(line):
        out = []
        col = 0
        for ch in line:
            if ch == "\t":
                spaces = 4 - (col % 4)
                out.append(" " * spaces)
                col += spaces
            else:
                out.append(ch)
                col += 1
        return "".join(out)

    def count_leading_spaces(s):
        return len(s) - len(s.lstrip(" "))

    def is_blank(line):
        return line.strip() == ""

    def is_whitespace(ch):
        return ch is None or ch.isspace()

    def is_punctuation(ch):
        return ch is not None and ch in string.punctuation

    def can_open_close(ch, prev_ch, next_ch):
        left_flanking = (not is_whitespace(next_ch)) and (
            not is_punctuation(next_ch)
            or is_whitespace(prev_ch)
            or is_punctuation(prev_ch)
        )
        right_flanking = (not is_whitespace(prev_ch)) and (
            not is_punctuation(prev_ch)
            or is_whitespace(next_ch)
            or is_punctuation(next_ch)
        )

        if ch == "*":
            can_open = left_flanking
            can_close = right_flanking
        else:
            can_open = left_flanking and (
                not right_flanking or is_punctuation(prev_ch)
            )
            can_close = right_flanking and (
                not left_flanking or is_punctuation(next_ch)
            )
        return can_open, can_close

    def is_hr(line):
        s = line.strip()
        if len(s) < 3:
            return False
        for c in ["*", "-", "_"]:
            t = s.replace(" ", "")
            if len(t) >= 3 and all(ch == c for ch in t):
                return True
        return False

    def atx_heading(line):
        m = re.match(r"^( {0,3})(#{1,6})([ \t]+|$)(.*)$", line)
        if not m:
            return None
        level = len(m.group(2))
        content = m.group(4)
        content = re.sub(r"[ \t]+#+[ \t]*$", "", content)
        return level, content

    def setext_underline(line):
        s = line.strip()
        if re.fullmatch(r"=+", s):
            return 1
        if re.fullmatch(r"-+", s):
            return 2
        return None

    def fence_start(line):
        m = re.match(r"^( {0,3})(`{3,}|~{3,})([^\n]*)$", line)
        if not m:
            return None
        fence = m.group(2)
        return {
            "indent": len(m.group(1)),
            "char": fence[0],
            "length": len(fence),
            "info": m.group(3).strip(),
        }

    def fence_close(line, opener):
        pattern = (
            r"^( {0,3})"
            + re.escape(opener["char"])
            + r"{"
            + str(opener["length"])
            + r",}[ \t]*$"
        )
        return re.match(pattern, line) is not None

    def indented_code(line):
        return count_leading_spaces(line) >= 4 and not is_blank(line)

    def blockquote_start(line):
        return re.match(r"^ {0,3}> ?(.*)$", line)

    def is_html_block_start(line):
        s = line.strip()
        return (
            re.match(r"^ {0,3}<(pre|script|style|textarea)([>\s]|$)", line, re.I)
            or s.startswith("<!--")
            or s.startswith("<?")
            or re.match(r"^ {0,3}<![A-Z]", line)
            or s.startswith("<![CDATA[")
            or re.match(
                r"^ {0,3}</?(address|article|aside|base|basefont|blockquote|body|"
                r"caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|"
                r"fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|"
                r"head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|"
                r"noframes|ol|optgroup|option|p|param|search|section|summary|table|"
                r"tbody|td|tfoot|th|thead|title|tr|track|ul)([ />]|$)",
                line,
                re.I,
            )
        ) is not None

    def html_block_type(line):
        s = line.strip()
        if re.match(r"^ {0,3}<(pre|script|style|textarea)([>\s]|$)", line, re.I):
            name = re.match(r"^ {0,3}<([A-Za-z]+)", line).group(1).lower()
            return ("tag", name)
        if s.startswith("<!--"):
            return ("until", "-->")
        if s.startswith("<?"):
            return ("until", "?>")
        if re.match(r"^ {0,3}<![A-Z]", line):
            return ("until", ">")
        if s.startswith("<![CDATA["):
            return ("until", "]]>")
        return ("blank", None)

    def match_list_marker(line):
        m = re.match(r"^( {0,3})([*+-])([ \t]+)(.*)$", line)
        if m:
            indent = len(m.group(1))
            marker = m.group(2)
            spaces = m.group(3)
            rest = m.group(4)
            return {
                "type": "ul",
                "indent": indent,
                "marker": marker,
                "content_col": indent + len(marker) + len(spaces),
                "rest": rest,
                "start": None,
            }

        m = re.match(r"^( {0,3})(\d{1,9})([.)])([ \t]+)(.*)$", line)
        if m:
            indent = len(m.group(1))
            number = int(m.group(2))
            delim = m.group(3)
            spaces = m.group(4)
            rest = m.group(5)
            return {
                "type": "ol",
                "indent": indent,
                "marker": m.group(2) + delim,
                "content_col": indent + len(m.group(2) + delim) + len(spaces),
                "rest": rest,
                "start": number,
            }

        return None

    def extract_references(lines):
        refs = {}
        kept = []
        ref_re = re.compile(
            r'^\s{0,3}\[([^\]]+)\]:\s*(\S+)(?:\s+(?:"([^"]*)"|\'([^\']*)\'|\(([^)]*)\)))?\s*$'
        )
        for line in lines:
            m = ref_re.match(line)
            if m:
                label = normalize_label(m.group(1))
                url = m.group(2)
                title = m.group(3) or m.group(4) or m.group(5)
                refs[label] = (url, title)
            else:
                kept.append(line)
        return refs, kept

    def parse_code_spans(text):
        result = []
        i = 0
        while i < len(text):
            if text[i] != "`":
                result.append(text[i])
                i += 1
                continue

            j = i
            while j < len(text) and text[j] == "`":
                j += 1
            ticks = j - i
            closer = "`" * ticks
            k = text.find(closer, j)
            if k == -1:
                result.append(text[i:j])
                i = j
                continue

            content = text[j:k]
            content = content.replace("\n", " ")
            if content.startswith(" ") and content.endswith(" ") and content.strip() != "":
                content = content[1:-1]
            result.append("<code>" + escape_html(content) + "</code>")
            i = k + ticks
        return "".join(result)

    def render_ref_link(label_text, ref_label):
        key = normalize_label(ref_label)
        if key not in refs:
            if ref_label == label_text:
                return "[" + label_text + "]"
            return "[" + label_text + "][" + ref_label + "]"
        url, title = refs[key]
        out = '<a href="' + html.escape(url, quote=True) + '"'
        if title:
            out += ' title="' + html.escape(title, quote=True) + '"'
        out += ">" + label_text + "</a>"
        return out

    def parse_links_images(text):
        text = re.sub(
            r'!\[([^\]]*)\]\(([^()\s]+)(?:\s+"([^"]*)")?\)',
            lambda m: '<img src="' + html.escape(m.group(2), quote=True) +
                      '" alt="' + html.escape(m.group(1), quote=True) + '"' +
                      (' title="' + html.escape(m.group(3), quote=True) + '"' if m.group(3) else "") +
                      " />",
            text,
        )

        text = re.sub(
            r'\[([^\]]+)\]\(([^()\s]+)(?:\s+"([^"]*)")?\)',
            lambda m: '<a href="' + html.escape(m.group(2), quote=True) + '"' +
                      (' title="' + html.escape(m.group(3), quote=True) + '"' if m.group(3) else "") +
                      ">" + m.group(1) + "</a>",
            text,
        )

        text = re.sub(
            r'\[([^\]]+)\]\[([^\]]*)\]',
            lambda m: render_ref_link(m.group(1), m.group(2) if m.group(2) else m.group(1)),
            text,
        )

        text = re.sub(
            r'\[([^\]]+)\]',
            lambda m: render_ref_link(m.group(1), m.group(1)),
            text,
        )

        return text

    def parse_emphasis(text):
        chars = list(text)
        delimiters = []
        i = 0
        while i < len(chars):
            if chars[i] not in "*_":
                i += 1
                continue
            ch = chars[i]
            j = i
            while j < len(chars) and chars[j] == ch:
                j += 1
            run_len = j - i
            prev_ch = chars[i - 1] if i > 0 else None
            next_ch = chars[j] if j < len(chars) else None
            can_open, can_close = can_open_close(ch, prev_ch, next_ch)
            delimiters.append({
                "pos": i,
                "end": j,
                "char": ch,
                "len": run_len,
                "can_open": can_open,
                "can_close": can_close,
            })
            i = j

        opens = {}
        closes = {}
        used = set()

        for c in range(len(delimiters)):
            closer = delimiters[c]
            if not closer["can_close"]:
                continue
            for o in range(c - 1, -1, -1):
                opener = delimiters[o]
                if not opener["can_open"]:
                    continue
                if opener["char"] != closer["char"]:
                    continue
                if opener["pos"] in used or closer["pos"] in used:
                    continue

                use_len = 2 if opener["len"] >= 2 and closer["len"] >= 2 else 1
                opens.setdefault(opener["pos"], []).append(use_len)
                closes.setdefault(closer["pos"], []).append(use_len)
                opener["len"] -= use_len
                closer["len"] -= use_len
                if opener["len"] == 0:
                    used.add(opener["pos"])
                if closer["len"] == 0:
                    used.add(closer["pos"])
                break

        out = []
        i = 0
        while i < len(chars):
            if i in opens:
                for n in sorted(opens[i], reverse=True):
                    out.append("<strong>" if n == 2 else "<em>")

            matched_delim = None
            for d in delimiters:
                if d["pos"] == i:
                    matched_delim = d
                    break

            if matched_delim is not None:
                run_len = matched_delim["end"] - matched_delim["pos"]
                remaining = matched_delim["len"]
                out.append(chars[i] * remaining)
                i = matched_delim["end"]
                if matched_delim["pos"] in closes:
                    for n in sorted(closes[matched_delim["pos"]], reverse=True):
                        out.append("</strong>" if n == 2 else "</em>")
                continue

            out.append(chars[i])
            i += 1

        return "".join(out)

    def parse_inline(text):
        text = escape_html(text)
        text = parse_code_spans(text)
        parts = re.split(r"(<code>.*?</code>)", text)
        for idx in range(len(parts)):
            if parts[idx].startswith("<code>") and parts[idx].endswith("</code>"):
                continue
            parts[idx] = parse_links_images(parts[idx])
            parts[idx] = parse_emphasis(parts[idx])
        return "".join(parts)

    class Node:
        def __init__(self, t, **kwargs):
            self.t = t
            self.attrs = kwargs
            self.children = kwargs.get("children", [])
            self.tight = kwargs.get("tight", False)

    def render(node, parent_tight=False):
        t = node.t

        if t == "document":
            return "".join(render(child) for child in node.children)

        if t == "paragraph":
            content = parse_inline(node.attrs["text"])
            if parent_tight:
                return content
            return "<p>" + content + "</p>\n"

        if t == "heading":
            level = node.attrs["level"]
            content = parse_inline(node.attrs["text"])
            return "<h" + str(level) + ">" + content + "</h" + str(level) + ">\n"

        if t == "thematic_break":
            return "<hr />\n"

        if t == "code_block":
            info = node.attrs.get("info", "").strip()
            code = escape_html(node.attrs["text"])
            if info:
                lang = html.escape(info.split()[0], quote=True)
                return '<pre><code class="language-' + lang + '">' + code + "</code></pre>\n"
            return "<pre><code>" + code + "</code></pre>\n"

        if t == "html_block":
            txt = node.attrs["text"]
            if txt.endswith("\n"):
                return txt
            return txt + "\n"

        if t == "blockquote":
            inner = "".join(render(child) for child in node.children).rstrip("\n")
            return "<blockquote>\n" + inner + "\n</blockquote>\n"

        if t == "list":
            tag = "ul" if node.attrs["list_type"] == "ul" else "ol"
            attrs = ""
            if tag == "ol" and node.attrs.get("start", 1) != 1:
                attrs = ' start="' + str(node.attrs["start"]) + '"'
            inner = "".join(render(child, parent_tight=node.tight) for child in node.children).rstrip("\n")
            return "<" + tag + attrs + ">\n" + inner + "\n</" + tag + ">\n"

        if t == "item":
            if len(node.children) == 1 and node.children[0].t == "paragraph":
                content = parse_inline(node.children[0].attrs["text"])
                return "<li>" + content + "</li>\n"

            if parent_tight:
                parts = []
                for child in node.children:
                    if child.t == "paragraph":
                        parts.append(parse_inline(child.attrs["text"]))
                    else:
                        parts.append(render(child, parent_tight=False).rstrip("\n"))
                inner = "".join(parts)
                return "<li>" + inner + "</li>\n"

            inner = "".join(render(child, parent_tight=False) for child in node.children).rstrip("\n")
            return "<li>" + inner + "</li>\n"

        return ""

    def parse_blocks(lines):
        nodes = []
        i = 0

        while i < len(lines):
            line = lines[i]

            if is_blank(line):
                i += 1
                continue

            h = atx_heading(line)
            if h:
                level, content = h
                nodes.append(Node("heading", level=level, text=content))
                i += 1
                continue

            if is_hr(line):
                nodes.append(Node("thematic_break"))
                i += 1
                continue

            opener = fence_start(line)
            if opener:
                i += 1
                buf = []
                while i < len(lines) and not fence_close(lines[i], opener):
                    buf.append(lines[i])
                    i += 1
                if i < len(lines):
                    i += 1
                text = "\n".join(buf)
                if buf:
                    text += "\n"
                nodes.append(Node("code_block", text=text, info=opener["info"]))
                continue

            if indented_code(line):
                buf = []
                while i < len(lines):
                    if is_blank(lines[i]):
                        buf.append("")
                        i += 1
                    elif indented_code(lines[i]):
                        buf.append(lines[i][4:])
                        i += 1
                    else:
                        break
                nodes.append(Node("code_block", text="\n".join(buf).rstrip("\n") + "\n", info=""))
                continue

            if blockquote_start(line):
                inner_lines = []
                while i < len(lines):
                    m = blockquote_start(lines[i])
                    if m:
                        inner_lines.append(m.group(1))
                        i += 1
                    elif is_blank(lines[i]):
                        inner_lines.append("")
                        i += 1
                    else:
                        break
                nodes.append(Node("blockquote", children=parse_blocks(inner_lines)))
                continue

            if is_html_block_start(line):
                kind = html_block_type(line)
                buf = [line]
                i += 1
                if kind[0] == "tag":
                    closing = "</" + kind[1] + ">"
                    while i < len(lines):
                        buf.append(lines[i])
                        if closing.lower() in lines[i].lower():
                            i += 1
                            break
                        i += 1
                elif kind[0] == "until":
                    stopper = kind[1]
                    while i < len(lines):
                        buf.append(lines[i])
                        if stopper in lines[i]:
                            i += 1
                            break
                        i += 1
                else:
                    while i < len(lines) and not is_blank(lines[i]):
                        buf.append(lines[i])
                        i += 1
                nodes.append(Node("html_block", text="\n".join(buf)))
                continue

            lm = match_list_marker(line)
            if lm:
                list_type = lm["type"]
                start = lm["start"] if list_type == "ol" else None
                items = []
                loose = False

                while i < len(lines):
                    cur = match_list_marker(lines[i])
                    if not cur or cur["type"] != list_type:
                        break

                    content_col = cur["content_col"]
                    item_lines = [cur["rest"]]
                    i += 1
                    had_blank = False

                    while i < len(lines):
                        if is_blank(lines[i]):
                            had_blank = True
                            item_lines.append("")
                            i += 1
                            if i < len(lines):
                                nxt = match_list_marker(lines[i])
                                if nxt and nxt["type"] == list_type:
                                    loose = True
                                    break
                            continue

                        nxt = match_list_marker(lines[i])
                        if nxt and nxt["type"] == list_type and count_leading_spaces(lines[i]) <= cur["indent"]:
                            break

                        if count_leading_spaces(lines[i]) >= content_col:
                            item_lines.append(lines[i][content_col:])
                            i += 1
                        else:
                            item_lines.append(lines[i])
                            i += 1

                    children = parse_blocks(item_lines)
                    if had_blank:
                        loose = True
                    items.append(Node("item", children=children))

                nodes.append(Node("list", list_type=list_type, start=start or 1, children=items, tight=not loose))
                continue

            para = [line]
            i += 1
            while i < len(lines) and not is_blank(lines[i]):
                if (
                    atx_heading(lines[i])
                    or is_hr(lines[i])
                    or fence_start(lines[i])
                    or blockquote_start(lines[i])
                    or match_list_marker(lines[i])
                    or is_html_block_start(lines[i])
                ):
                    break
                para.append(lines[i])
                i += 1

            if i < len(lines):
                lvl = setext_underline(lines[i])
                if lvl and len(para) == 1:
                    nodes.append(Node("heading", level=lvl, text=para[0].strip()))
                    i += 1
                    continue

            text = " ".join(x.strip() for x in para)
            nodes.append(Node("paragraph", text=text))

        return nodes

    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    markdown = re.sub(r'(?<=\S)\s+([-*+]|\d+[.)])\s+', r'\n\1 ', markdown)
    raw_lines = markdown.split("\n")

    lines = [detab(line) for line in raw_lines]

    refs, lines = extract_references(lines)
    root = Node("document", children=parse_blocks(lines))
    html_output = render(root)
    return html_output.rstrip() + "\n"

