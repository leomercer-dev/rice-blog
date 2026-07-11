#!/usr/bin/env python3
"""Rice Blog Build System - Jinja2 static site generator."""

import os, sys, glob, shutil, yaml, re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape, BaseLoader

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "_site")
INC_DIR = os.path.join(BASE, "_includes")
SRC_DIR = os.path.join(BASE, "src")
DATA_DIR = os.path.join(BASE, "data")


class MultiDirLoader(BaseLoader):
    """Load templates from multiple directories."""
    def __init__(self, dirs):
        super().__init__()
        self.dirs = [os.path.normpath(d) for d in dirs]
    
    def get_source(self, env, template):
        for d in self.dirs:
            path = os.path.join(d, template)
            if os.path.isfile(path):
                with open(path) as f:
                    src = f.read()
                return src, path, (lambda: True)
        raise Exception(f"Template not found: {template} (searched in {self.dirs})")


def jinja_env():
    """Get Jinja2 environment that searches both BASE and _includes."""
    return Environment(
        loader=MultiDirLoader([BASE, INC_DIR]),
        autoescape=select_autoescape(["html", "xml"]),
    )


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_data():
    data = {}
    for fp in glob.glob(os.path.join(DATA_DIR, "*.yaml")):
        key = os.path.splitext(os.path.basename(fp))[0]
        data[key] = load_yaml(fp)
    return data


def md_to_html(md_text):
    """Simple markdown to HTML converter."""
    lines = md_text.split("\n")
    out = []
    in_code = False
    code_lang = "text"
    in_list = False

    for line in lines:
        if line.startswith("```"):
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                lang = line[3:].strip() or "text"
                out.append('<pre><code class="language-' + lang + '">')
                in_code = True
            continue

        if in_code:
            out.append(line)
            continue

        hm = re.match(r"^(#{1,6})\s+(.*)", line)
        if hm:
            lvl = len(hm.group(1))
            text = re.sub(r"`([^`]+)`", r"<code>\1</code>", hm.group(2).strip())
            out.append(f"<h{lvl}>{text}</h{lvl}>")
            if in_list:
                out.append("</ul>")
                in_list = False
            continue

        if re.match(r"^[-*]\s+", line):
            item = re.sub(r"^[-*]\s+", "", line.strip())
            item = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", item)
            item = re.sub(r"`([^`]+)`", r"<code>\1</code>", item)
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{item}</li>")
            continue

        if line.strip() == "":
            if in_list:
                out.append("</ul>")
                in_list = False
            continue

        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
        if text.strip():
            out.append(f"<p>{text}</p>")

    if in_code:
        out.append("</code></pre>")
    if in_list:
        out.append("</ul>")

    return "\n".join(out)


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def get_context(data):
    rices = sorted(data.get("rices", {}).get("rice", []), key=lambda x: x.get("date", ""), reverse=True)
    posts = sorted(data.get("posts", {}).get("posts", []), key=lambda x: x.get("date", ""), reverse=True)
    return {"rices": rices, "posts": posts, "year": datetime.now().year}


def render_template(filename, context):
    """Render a .html file at BASE_DIR using Jinja2."""
    env = jinja_env()
    template = env.get_template(filename)
    return template.render(**context)


def build(data):
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    ctx = get_context(data)
    print("Building rice.blog...")

    # Static pages with full jinja context
    for page in ["index.html", "rice.html", "posts.html", "about.html"]:
        html = render_template(page, ctx)
        write_file(os.path.join(OUT, page), html)
        print(f"  ✓ {page}")

    # Individual rice post pages (using src/ templates)
    for rice in ctx["rices"]:
        if rice.get("status") == "draft":
            continue
        tpl_path = os.path.join(SRC_DIR, "rice-post.html.j2")
        with open(tpl_path) as f:
            tpl_str = f.read()
        env = jinja_env()
        html = env.from_string(tpl_str).render(rice=rice, year=ctx["year"])
        write_file(os.path.join(OUT, f"rice-{rice['id']}.html"), html)
        print(f"  ✓ rice-{rice['id']}.html")

    # Individual blog post pages
    for post in ctx["posts"]:
        if post.get("draft"):
            continue
        md_path = os.path.join(BASE, "src", "posts", f"{post['id']}.md")
        if os.path.exists(md_path):
            with open(md_path) as f:
                html_content = md_to_html(f.read())
        else:
            html_content = "<p>Post content pending.</p>"

        tpl_path = os.path.join(SRC_DIR, "post-page.html.j2")
        with open(tpl_path) as f:
            tpl_str = f.read()
        env = jinja_env()
        html = env.from_string(tpl_str).render(
            post=post, post_content=html_content, year=ctx["year"]
        )
        write_file(os.path.join(OUT, f"posts-{post['id']}.html"), html)
        print(f"  ✓ posts-{post['id']}.html")

    # Copy assets
    src_assets = os.path.join(BASE, "assets")
    if os.path.exists(src_assets):
        shutil.copytree(src_assets, os.path.join(OUT, "assets"))
    
    # Copy rice screenshots
    src_imgs = os.path.join(BASE, "assets", "img", "rice")
    dst_imgs = os.path.join(OUT, "assets", "img", "rice")
    if os.path.exists(src_imgs):
        if os.path.exists(dst_imgs):
            shutil.rmtree(dst_imgs)
        shutil.copytree(src_imgs, dst_imgs)
    
    print("  ✓ assets/")
    print(f"Done! Output: {OUT}")


if __name__ == "__main__":
    build(load_data())
