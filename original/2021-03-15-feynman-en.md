---
audio: false
generated: false
image: true
lang: en
layout: post
title: 'mathjax2mobi: Converting MathJax HTML for eBooks'
translated: true
type: post
---

*This blog post was translated by ChatGPT.*

---

### Project Overview

Let’s briefly discuss the project.

![feynman_online](assets/images/feynman/feynman_online.jpg)

<img src="/assets/images/feynman/change.JPG" alt="change" style="zoom:50%;" />

![latex](assets/images/feynman/latex.JPG)

![epub_black](assets/images/feynman/epub_black.JPG)

![epub_beautiful](assets/images/feynman/epub_beautiful.JPG)

I felt a bit happy after completing the project. I wrote the following paragraph:

After coding for a day, I finally got a beautiful eBook of Feynman's Lectures on Physics! The Feynman Lectures on Physics are available online, rendered using `latex`. People often use `latex` to write papers because it renders mathematical formulas excellently. For the online version, the `mathjax` library is used. It converts `latex` source code into `html` code, generating many `div` and `span` tags. However, eBooks do not support this method. So, the idea was to scrape the webpage, reverse the `mathjax` rendering, and replace it with `svg` images. There were quite a few problems. One issue was that the source code had many custom `latex` macros that needed to be added. The second issue was that embedding many `svg` images caused problems. While a single `svg` is fine, many can cause issues, likely due to browser and `svg` bugs. To solve this, the `svg` images were saved as files and included with `img` tags. Formulas were also divided into two types: those in the middle of text and those that stood alone. In the end, I got a beautiful eBook!

### Reference Materials

Here, I document the resources accessed during the project. Since this is a tutorial, it also shows students what it’s like to work on a project.

![](assets/images/feynman/s1.PNG)

![](assets/images/feynman/s2.PNG)

![](assets/images/feynman/s3.PNG)

![](assets/images/feynman/s4.PNG)

![](assets/images/feynman/s5.PNG)

![](assets/images/feynman/s6.PNG)

![](assets/images/feynman/s7.PNG)

![](assets/images/feynman/s8.PNG)

### Starting the Project

The Feynman Lectures on Physics are publicly available online for reading. I wanted to read them on a `Kindle`. However, since they contain many mathematical formulas, the original manuscript was likely done using `latex`. The content is displayed on the web using the `mathjax` library.

Here’s an example:

```html
<span class="MathJax_Preview" style="color: inherit; display: none;">
</span>
<div class="MathJax_Display">
    <span class="MathJax MathJax_FullWidth" id="MathJax-Element-10-Frame" tabindex="0" style="">
              <span class="mi" id="MathJax-Span-159" style="font-family: MathJax_Math-italic;">d<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.003em;">
                </span>
    </span>
</div>
<script type="math/tex; mode=display" id="MathJax-Element-10">\begin{equation}
\label{Eq:I:13:3}
dT/dt = Fv.
\end{equation}
</script>
```

The above is a snippet of `html` code. The `latex` raw text is within the `script` tag. `mathjax` turns it into many `span` tags for display.

Our idea now is to change `mathjax`'s display method to `svg` images.

Found a project `tuxu/latex2svg` on GitHub.

```python
from latex2svg import latex2svg
out = latex2svg(r'\( e^{i \pi} + 1 = 0 \)')
print(out['depth'])
print(out['svg'])
```

Tried running it, but encountered an error.

```shell
    raise RuntimeError('latex not found')
RuntimeError: latex not found
```

Let's check the code.

```python
    # Run LaTeX and create DVI file
    try:
        ret = subprocess.run(shlex.split(params['latex_cmd']+' code.tex'),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             cwd=working_directory)
        ret.check_returncode()
    except FileNotFoundError:
        raise RuntimeError('latex not found')
```

It turns out this also relies on the `latex` command.

Let's install it.

```shell
brew install --cask mactex
==> Caveats
You must restart your terminal window for the installation of MacTex CLI tools to take effect.
Alternatively, Bash and Zsh users can run the command:
  eval "$(/usr/libexec/path_helper)"
==> Downloading http://mirror.ctan.org/systems/mac/mactex/mactex-20200407.pkg
==> Downloading from https://mirrors.aliyun.com/CTAN/systems/mac/mactex/mactex-20200407.pkg
######################################################################## 100.0%
All formula dependencies satisfied.
==> Installing Cask mactex
==> Running installer for mactex; your password may be necessary.
installer: Package name is MacTeX
installer: choices changes file '/private/tmp/choices20210315-4643-5884ro.xml' applied
installer: Installing at base path /
installer: The install was successful.
🍺  mactex was successfully installed!
```

Installation successful.

```shell
% latex
This is pdfTeX, Version 3.14159265-2.6-1.40.21 (TeX Live 2020) (preloaded format=latex)
 restricted \write18 enabled.
**
```

```python
out = latex2svg(r'\( e^{i \pi} + 1 = 0 \)')
print(out['depth'])
print(out['svg'])

svg = open('1.svg', 'w')
svg.write(out['svg'])
svg.close()
```

`svg` generation is successful.

So, let's try generating `svg` from the `latex` text obtained from `mathjax`.

```python
from bs4 import BeautifulSoup
from latex2svg import latex2svg

file = open('The Feynman Lectures on Physics Vol. I Ch. 13_ Work and Potential Energy (A).html')
content = file.read()

soup = BeautifulSoup(content)

mathjaxs = soup.findAll('script', {'type': 'math/tex'})
for mathjax in mathjaxs:
    print(mathjax.string)
    out = latex2svg(mathjax.string)
    print(out['svg'])
```

Unfortunately, it threw an error.

```python
    raise CalledProcessError(self.returncode, self.args, self.stdout,
subprocess.CalledProcessError: Command '['latex', '-interaction', 'nonstopmode', '-halt-on-error', 'code.tex']' returned non-zero exit status 1.
```

Which formula caused the error?

```latex
\tfrac{1}{2}mv^2
```

## LaTeX

Let’s learn some `latex`.

```latex
\documentclass[12pt]{article}
\usepackage{lingmacros}
\usepackage{tree-dvips}
\begin{document}

\section*{Notes for My Paper}

Don't forget to include examples of topicalization.
They look like this:

{\small
\enumsentence{Topicalization from sentential subject:\\
\shortex{7}{a John$_i$ [a & kltukl & [el &
  {\bf l-}oltoir & er & ngii$_i$ & a Mary]]}
{ & {\bf R-}clear & {\sc comp} &
  {\bf IR}.{\sc 3s}-love   & P & him & }
{John, (it's) clear that Mary loves (him).}}
}

\subsection*{How to handle topicalization}

I'll just assume a tree structure like (\ex{1}).

{\small
\enumsentence{Structure of A$'$ Projections:\\ [2ex]
\begin{tabular}[t]{cccc}
    & \node{i}{CP}\\ [2ex]
    \node{ii}{Spec} &   &\node{iii}{C$'$}\\ [2ex]
        &\node{iv}{C} & & \node{v}{SAgrP}
\end{tabular}
\nodeconnect{i}{ii}
\nodeconnect{i}{iii}
\nodeconnect{iii}{iv}
\nodeconnect{iii}{v}
}
}

\subsection*{Mood}

Mood changes when there is a topic, as well as when
there is WH-movement.  \emph{Irrealis} is the mood when
there is a non-subject topic or WH-phrase in Comp.
\emph{Realis} is the mood when there is a subject topic
or WH-phrase.

\end{document}
```

Found a sample `latex` source code online.

```shell
% latex code.tex
This is pdfTeX, Version 3.14159265-2.6-1.40.21 (TeX Live 2020) (

preloaded format=latex)
 restricted \write18 enabled.
entering extended mode
(./code.tex
LaTeX2e <2020-02-02> patch level 5
L3 programming layer <2020-03-06>
(/usr/local/texlive/2020/texmf-dist/tex/latex/base/article.cls
Document Class: article 2019/12/20 v1.4l Standard LaTeX document class
(/usr/local/texlive/2020/texmf-dist/tex/latex/base/size12.clo))
(/usr/local/texlive/2020/texmf-dist/tex/latex/tree-dvips/lingmacros.sty)
(/usr/local/texlive/2020/texmf-dist/tex/latex/tree-dvips/tree-dvips.sty
tree-dvips version .91 of May 16, 1995
) (/usr/local/texlive/2020/texmf-dist/tex/latex/l3backend/l3backend-dvips.def)
(./code.aux) [1] (./code.aux) )
Output written on code.dvi (1 page, 3416 bytes).
Transcript written on code.log.
```

![latex](assets/images/feynman/latex.png)

Let’s look at the source code and the rendered effect to see what we can learn.

```latex
\begin{document}
\end{document}
```

This wraps the document.

```latex
\section*{Notes for My Paper}
```

This denotes the section title.

```latex
\subsection*{How to handle topicalization}
```

This denotes a subsection title.

```latex
\shortex{7}{a John$_i$ [a & kltukl & [el &
  {\bf l-}oltoir & er & ngii$_i$ & a Mary]]}
```

![shortex](assets/images/feynman/shortex.png)

You can see that `$_i$` denotes a subscript. `{\bf l-}` denotes bold text.

```latex
\enumsentence{Structure of A$'$ Projections:\\ [2ex]
\begin{tabular}[t]{cccc}
    & \node{i}{CP}\\ [2ex]
    \node{ii}{Spec} &   &\node{iii}{C$'$}\\ [2ex]
        &\node{iv}{C} & & \node{v}{SAgrP}
\end{tabular}
\nodeconnect{i}{ii}
\nodeconnect{i}{iii}
\nodeconnect{iii}{iv}
\nodeconnect{iii}{v}
}
```

<img src="/assets/images/feynman/node.png" alt="node" style="zoom:50%;" />

Note that `nodeconnect` denotes connections.

### Converting LaTeX to SVG

Continuing the project.

```latex
\documentclass[16pt]{article}
\usepackage{amsmath}
\begin{document}

\[\tfrac{1}{2}mv^2\]

\end{document}
```

<img src="/assets/images/feynman/frac.png" alt="frac" style="zoom:50%;" />

This renders correctly. The failure to render in code might be due to the absence of `\usepackage{amsmath}`.

```latex
\documentclass[12pt,preview]{standalone}

\usepackage[utf8x]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{newtxtext}
\usepackage[libertine]{newtxmath}

\begin{document}
\begin{preview}
\tfrac{1}{2}mv^2
\end{preview}
\end{document}
```

```shell
! Missing $ inserted.
<inserted text>
                $
l.12 \tfrac{1}{2}
                 mv^2
```

This caused an error. Changing it as follows works:

```latex
\[\tfrac{1}{2}mv^2\]
```

Continuing with various attempts.

```python
from bs4 import BeautifulSoup
from latex2svg import latex2svg

file = open('The Feynman Lectures on Physics Vol. I Ch. 13_ Work and Potential Energy (A).html')
content = file.read()

soup = BeautifulSoup(content, features="lxml")

mathjaxs = soup.findAll('script', {'type': 'math/tex'})
for mathjax in mathjaxs:
    print(mathjax.string)
    wrap = '$' + mathjax.string + '$'
    # if 'frac' in mathjax.string:
    #     wrap = '$' + mathjax.string + '$'
    if 'FLP' in mathjax.string:
        continue
    elif 'Fig' in mathjax.string:
        continue
    elif 'eps' in mathjax.string:
        continue
    out = latex2svg(wrap)
    # print(out)
    node = BeautifulSoup(out['svg'], features="lxml")
    svg = node.find('svg')
    mathjax.insert_after(svg)
    # print(out['svg'])
    # break
    # mathjax.replaceWith(out['svg'])

    # print(dir(mathjax))
    # break

    # out = latex2svg(wrap)
    # print(out['svg'])

# print(len(soup.contents))

output_file = open('out.html', 'w')
output_file.write(soup.prettify())
output_file.close()
# print(soup.contents)

# out = latex2svg(r'\( e^{i \pi} + 1 = 0 \)')
# print(out['depth'])
# print(out['svg'])

# svg = open('1.svg', 'w')
# svg.write(out['svg'])
# svg.close()

```

What exactly was I trying here?

```python
    if 'FLP' in mathjax.string:
        continue
    elif 'Fig' in mathjax.string:
        continue
    elif 'eps' in mathjax.string:
        continue
```

When parsing the `latex` source with `FLP`, `Fig`, or `eps`, the conversion process failed.

For example, in the `HTML`, there is this script:

```html
<script type="math/tex" id="MathJax-Element-11">\FLPF\cdot\FLPv</script>
```

Parsed to:

```latex
\FLPF\cdot\FLPv
```

When converting in code, it failed. That is, `latex2svg.py` failed. This uses the `latex` program for conversion.

`code.tex`:

```latex
\documentclass[12pt,preview]{standalone}

\usepackage[utf8x]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{newtxtext}
\usepackage[libertine]{newtxmath}

\begin{document}
\begin{preview}
\begin{equation}
    \FLPF\cdot\FLPv
\end{equation}
\end{preview}
\end{document}
```

```shell
$latex code.tex
! Undefined control sequence.
l.13     \FLPF
              \cdot\FLPv
?
```

What exactly is the problem? Later, I noticed this code in the `html`.

```html
<script type="text/x-mathjax-config;executed=true">
      MathJax.Hub.Config({
        TeX: {
          Macros: {
            FLPvec: ["\\boldsymbol{#1}", 1], Figvec: ["\\mathbf{#1}", 1], FLPC: ["\\FLPvec{C}", 0], FLPF: ["\\FLPvec{F}", 0], FLPa: ["\\FLPvec{a}", 0], FLPb: ["\\FLPvec{b}", 0], FLPr: ["\\FLPvec{r}", 0], FLPs: ["\\FLPvec{s}", 0], FLPv: ["\\FLPvec{v}", 0], ddt: ["\\frac{d#1}{d#2}", 2], epsO: ["\\epsilon_0", 0], FigC: ["\\Figvec{C}", 0]
          }
        }
      });
</script>
```

This shows that during rendering, macros were set for `MathJax`. Therefore, these macros should also be added to our `latex` conversion source. Let's add them.

```latex
\documentclass[12pt,preview]{standalone}

\usepackage[utf8x]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{newtxtext}
\usepackage[libertine]{newtxmath}

\newcommand{\FLPvec}[1]{\boldsymbol{#1}}
\newcommand{\Figvec}[1]{\mathbf{#1}}
\newcommand{\FLPC}{\FLPvec{C}}
\newcommand{\FLPF}{\FLPvec{F}}
\newcommand{\FLPa}{\FLPvec{a}}
\newcommand{\FLPb}{\FLPvec{a}}
\newcommand{\FLPr}{\FLPvec{r}}
\newcommand{\FLPs}{\FLPvec{s}}
\newcommand{\FLPv}{\FLPvec{v}}
\newcommand{\ddt}[2]{\frac{d#1}{d#2}}
\

newcommand{\epsO}{\epsilon_0}
\newcommand{\FigC}{\Figvec{C}}
\begin{document}
\begin{preview}
\begin{equation}
    \FLPF\cdot\FLPv
\end{equation}
\end{preview}
\end{document}
```

This works.

![fv1](assets/images/feynman/fv1.png)

### Analyzing the Code

Let's look at the final code.

```python
import subprocess
from bs4 import BeautifulSoup
from latex2svg import latex2svg

def clean_mathjax(soup, name, cls):
    previews = soup.findAll(name, {'class': cls})
    for preview in previews:
        preview.decompose()

def clean_script(soup):
    scripts = soup.findAll('script')
    for s in scripts:
        s.decompose()

def wrap_latex(mathjax, equation = False):
    wrap = ''
    if equation:
        wrap = mathjax.string
    else:
        wrap = '$' + mathjax.string + '$'
    wrap = wrap.replace('label', 'tag')
    return wrap

def wrap_svg(svg, equation):
    if equation:
        p = BeautifulSoup(f'<div style="text-align:center;"></div>', features="lxml")
        p.div.append(svg)
        return p.div
    else:
        return svg

def to_svg(mathjaxs, equation=False):
    if equation:
        svg_prefix = 'eq_'
    else:
        svg_prefix = 'in_'
    i = 0
    for mathjax in mathjaxs:
        print(mathjax.string)
        wrap = wrap_latex(mathjax, equation=equation)
        out = {}
        try:
            out = latex2svg(wrap)
        except subprocess.CalledProcessError as err:
            raise err

        f = open(f'svgs/{svg_prefix}{i}.svg', 'w')
        f.write(out['svg'])
        f.close()

        node = BeautifulSoup('<img>', features="lxml")
        img = node.find('img')
        img.attrs['src'] = f'./svgs/{svg_prefix}{i}.svg'
        img.attrs['style'] = 'vertical-align: middle; margin: 0.5em 0;'

        p = wrap_svg(img, equation)
        mathjax.insert_after(p)
        i +=1

def main():
    file = open('The Feynman Lectures on Physics Vol. I Ch. 13_ Work and Potential Energy (A).html')
    content = file.read()

    soup = BeautifulSoup(content, features="lxml")
    clean_mathjax(soup, 'span', 'MathJax')
    clean_mathjax(soup, 'div', 'MathJax_Display')
    clean_mathjax(soup, 'span', 'MathJax_Preview')

    mathjaxs = soup.findAll('script', {'type': 'math/tex'})
    to_svg(mathjaxs, equation=False)

    mathjaxs = soup.findAll('script', {'type': 'math/tex; mode=display'})
    to_svg(mathjaxs, equation=True)

    clean_script(soup)

    output_file = open('out.html', 'w')
    output_file.write(soup.prettify())
    output_file.close()

main()
```

When we want to convert the entire eBook, we can start with a single page.

```python
    file = open('The Feynman Lectures on Physics Vol. I Ch. 13_ Work and Potential Energy (A).html')
    content = file.read()
```

Here, a single page is downloaded.

`MathJax` generates many `div` and `span` tags. For example, the equation `T+U=const` generates:

```html
<span class="MathJax">T</span>
<span class="MathJax">+</span>
<span class="MathJax">U</span>
<span class="MathJax">=</span>
<span class="MathJax">const</span>
```

These are annoying and affect the text because we already have `svg`. So, they are unnecessary.

```python
def clean_mathjax(soup, name, cls):
    previews = soup.findAll(name, {'class': cls})
    for preview in previews:
        preview.decompose()

    clean_mathjax(soup, 'span', 'MathJax')
    clean_mathjax(soup, 'div', 'MathJax_Display')
    clean_mathjax(soup, 'span', 'MathJax_Preview')
```

Remove them all.

```python
    mathjaxs = soup.findAll('script', {'type': 'math/tex'})
    to_svg(mathjaxs, equation=False)

    mathjaxs = soup.findAll('script', {'type': 'math/tex; mode=display'})
    to_svg(mathjaxs, equation=True)
```

Note that here we have two types of `script`.

```latex
m(dv/dt)=F
```

This is an inline formula.

```latex
\begin{equation}
\underset{\text{K.E.}}{\tfrac{1}{2}mv^2}+
\underset{\text{P.E.}}{\vphantom{\tfrac{1}{2}}mgh}=\text{const},\notag
```

This is a standalone formula.

For inline formulas, you need to add `$` or `[]` around the expression to avoid errors.

```latex
\begin{document}
\begin{preview}
\tfrac{1}{2}mv^2
\end{preview}
\end{document}
```

```shell
! Missing $ inserted.
<inserted text>
                $
l.26 \tfrac{1}{2}
                 mv^2
```

It should be changed to:

```latex
\begin{document}
\begin{preview}
$\tfrac{1}{2}mv^2$
\end{preview}
\end{document}
```

Next, let's see how to convert `latex` to `svg`.

```python
    if equation:
        svg_prefix = 'eq_'
    else:
        svg_prefix = 'in_'
```

```shell
% tree svgs
svgs
├── eq_0.svg
├── eq_1.svg
├── in_0.svg
```

This saves the `svg`.

```python
def wrap_latex(mathjax, equation = False):
    wrap = ''
    if equation:
        wrap = mathjax.string
    else:
        wrap = '$' + mathjax.string + '$'
    wrap = wrap.replace('label', 'tag')
    return wrap
```

Here, the `latex` source is adjusted. Note that `label` is changed to `tag`.

![tag](assets/images/feynman/tag.png)

Note the right `Eq: I: 13:14`. If it is `label`, it fails to parse correctly, displaying `(1)`. So, `tag` is used temporarily.

Next, `latex2svg.py` is called.

```python
        out = {}
        try:
            out = latex2svg(wrap)
        except subprocess.CalledProcessError as err:
            raise err
```

Let's look at `latex2svg.py`.

```python
    # Run LaTeX and create DVI file
    try:
        ret = subprocess.run(shlex.split(params['latex_cmd']+' code.tex'),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             cwd=working_directory)
        ret.check_returncode()
    except FileNotFoundError:
        raise RuntimeError('latex not found')
```

This calls the `latex` command.

```shell
 % latex --help
Usage: pdftex [OPTION]... [TEXNAME[.tex]] [COMMANDS]
   or: pdftex [OPTION]... \FIRST-LINE
   or: pdftex [OPTION]... &FMT ARGS
  Run pdfTeX on TEXNAME, usually creating TEXNAME.pdf.
```

```python
    try:
        ret = subprocess.run(shlex.split(params['dvisvgm_cmd']+' code.dvi'),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             cwd=working_directory, env=env)
        ret.check_returncode()
    except FileNotFoundError:
        raise RuntimeError('dvisvgm not found')
```

This calls the `dvisvgm` command.

```shell
% dvisvgm
dvisvgm 2.9.1

This program converts DVI files, as created by TeX/LaTeX, as well as
EPS and PDF files to the XML-based scalable vector graphics format SVG.

Usage: dvisvgm [options] dvifile
       dvisvgm --eps [options] epsfile
       dvisvgm --pdf [options] pdffile
```

Where do we write the `latex` custom macros? Here, we need to modify `latex2svg.py` to change `default_preamble`.

```python
default_preamble = r"""
\usepackage[utf8x]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{newtxtext}
\usepackage[libertine]{newtxmath}

\newcommand{\FLPvec}[1]{\boldsymbol{#1}}
\newcommand{\Figvec}[1]{\mathbf{#1}}
\newcommand{\FLPC}{\FLPvec{C}}
\newcommand{\FLPF}{\FLP

vec{F}}
\newcommand{\FLPa}{\FLPvec{a}}
\newcommand{\FLPb}{\FLPvec{a}}
\newcommand{\FLPr}{\FLPvec{r}}
\newcommand{\FLPs}{\FLPvec{s}}
\newcommand{\FLPv}{\FLPvec{v}}
\newcommand{\ddt}[2]{\frac{d#1}{d#2}}
\newcommand{\epsO}{\epsilon_0}
\newcommand{\FigC}{\Figvec{C}}
"""
```

After successful conversion, write to a file.

```python
        f = open(f'svgs/{svg_prefix}{i}.svg', 'w')
        f.write(out['svg'])
        f.close()
```

Continue.

```python
        node = BeautifulSoup('<img>', features="lxml")
        img = node.find('img')
        img.attrs['src'] = f'./svgs/{svg_prefix}{i}.svg'
        img.attrs['style'] = 'vertical-align: middle; margin: 0.5em 0;'
```

Here, an `img` tag is constructed.

```python
def wrap_svg(svg, equation):
    if equation:
        p = BeautifulSoup(f'<div style="text-align:center;"></div>', features="lxml")
        p.div.append(svg)
        return p.div
    else:
        return svg

p = wrap_svg(img, equation)
```

For standalone `latex`, wrap it with a `div` and center it.

```python
mathjax.insert_after(p)
```

Here, the `div` or `img` tag is added after the original `script`.

```python
def clean_script(soup):
    scripts = soup.findAll('script')
    for s in scripts:
        s.decompose()

clean_script(soup)
```

After replacing all `latex` with `svg`, `script` tags are no longer needed, so remove them for a cleaner result.

Finally, write the modified entire `html` to a file.

```python
    output_file = open('out.html', 'w')
    output_file.write(soup.prettify())
    output_file.close()
```

Then, use the `pandoc` tool to convert to `epub`.

```shell
pandoc -s -r html out.html -o feynman.epub
```

This will open a beautiful eBook.

Why not embed `svg` tags directly and instead use `img` tags? For example, writing it like this:

```html
<p></p>
<svg></svg>
<p></p>
```

There’s a very strange bug. When there are many `svg`, the following happens:

<img src="/assets/images/feynman/svg_p1.png" alt="svg_p1" style="zoom:40%;" />

Later, I found that using `img` works. As to why, I haven’t figured it out. When I took a single `svg` out and viewed it in a browser, there was no problem. It seems that when the browser renders many `svg`, it fails.

### Finally

As for how to convert `epub` to `mobi`, you can use the official `Kindle` tool `Kindle Previewer 3`. Note that this is just one chapter.

The project code is available at [feynman-lectures-mobi@lzwjava](https://github.com/lzwjava/feynman-lectures-mobi).

How to scrape and organize all the pages into an eBook will be discussed later. But a single chapter of the Feynman Lectures on Physics is enough for now. Alright, let’s pick up the Kindle and start reading!
