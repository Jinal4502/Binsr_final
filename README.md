
# 🏡 Binsr Final — Unified Inspection Report Generator

This project generates **property inspection reports** in two distinct formats:

1. **🧱 TREC Report (TypeScript)** — official TREC-style inspection form built with Node.js and `pnpm`.
2. **🧾 Binsr Customized Report (Python)** — a visually enhanced HTML → PDF report using **Jinja2** and **WeasyPrint**.

Both are combined inside a single **Streamlit dashboard** (`app.py`) that allows you to upload an `inspection.json` and download final PDFs instantly.

---

## 🗂️ Folder Structure

```plaintext
Binsr_final/
│
├── app.py                        # Streamlit dashboard (main entry)
├── README.md                     # Documentation (this file)
│
├── binsr-challenge/              # TREC Report generator (TypeScript)
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── tsconfig.json
│   ├── src/
│   │   ├── inspection.json           # Input JSON file
│   │   ├── generate_report.ts        # Main TypeScript report generator
│   │   ├── generate_first_page.ts
│   │   └── generate_other_pages.ts
│   └── output/
│       └── trec_report.pdf       # ✅ Final TREC PDF output
│
└── bonus/                        # Binsr Custom Report generator (Python)
    ├── inspection_report_html.py     # HTML → PDF generator
    ├── binsr_customized_inspection_report.pdf    # ✅ Final Binsr PDF output
    └── templates/
        └── report_template.html      # Jinja2 template for layout/styling
````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/Binsr_final.git
cd Binsr_final
```

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3️⃣ Install dependencies

```bash
pip install streamlit jinja2 weasyprint cairocffi cffi tinycss2 cssselect2 pillow requests
```

> 💡 On macOS, install WeasyPrint’s native libraries:
>
> ```bash
> brew install cairo pango gdk-pixbuf libffi pygobject3
> ```

---

## 🚀 Run the Streamlit App

```bash
streamlit run app.py
```

Then open the local link (usually [http://localhost:8501](http://localhost:8501)) in your browser.

---

## 🧩 Streamlit Dashboard Overview

### 🗂 Upload Section

* Upload your own `inspection.json` file (optional).
* If no file is uploaded, the app uses the default JSON at:

  ```
  binsr-challenge/src/inspection.json
  ```

### ⚙️ Report Options

Choose which reports to generate:

* **🧱 TREC Report (TypeScript)** — runs the Node pipeline
* **🧾 Binsr Customized Report (Python)** — runs the Jinja2/WeasyPrint generator

Each generation shows progress, total time, and direct PDF download buttons.

---

## 📍 Output Locations

| Report Type                 | Description               | Output Path                                  |
| --------------------------- | ------------------------- | -------------------------------------------- |
| **TREC Report**             | Official inspection form  | `binsr-challenge/output/combined_report.pdf` |
| **Binsr Customized Report** | HTML → PDF via WeasyPrint | `bonus/inspection_report_html.pdf`           |
| **Default (Both)**          | Generates both            | Both of the above                            |

---

## ⚡ Command-Line Alternatives

### Run the Python (Binsr) report only:

```bash
python bonus/inspection_report_html.py
```

### Run the Node.js (TREC) report only:

```bash
cd binsr-challenge
pnpm i
npx ts-node src/generate_report.ts
```

---

## 🧰 Requirements Summary

### Python 3.10+

Install with:

```bash
pip install streamlit jinja2 weasyprint cairocffi cffi tinycss2 cssselect2 pillow requests
```

### Node.js + pnpm

Install globally:

```bash
npm install -g pnpm
```

---

## 🧠 Troubleshooting

### ⚠️ macOS: “cannot load library 'libgobject-2.0-0'”

```bash
brew install cairo pango gdk-pixbuf libffi pygobject3
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib
```

### ⚠️ Node: `ERR_PNPM_NO_PKG_MANIFEST`

Run pnpm from the correct folder:

```
Binsr_final/binsr-challenge/
```

### ⚠️ Streamlit stops after TREC run

Avoid `os.chdir()`.
Always run commands like this:

```python
subprocess.run([...], check=True, cwd=CHALLENGE_DIR)
```

---

## 🕒 Typical Timings

| Report                | Avg Time | Description                         |
| --------------------- | -------- | ----------------------------------- |
| **Binsr (Python)**    | ~12-13 s | Full HTML → PDF via WeasyPrint      |
| **TREC (TypeScript)** | ~7–8 s   | Node pipeline with headless browser |
| **Default (Both)**    | ~20-22 s | Sequential combined run             |

---

## 🧩 Developer Notes

* Streamlit uses `subprocess.run(..., cwd=...)` to keep its working directory stable.
* No `os.chdir()` calls are used — prevents reload errors.
* TREC generator runs once (`await generateReport(false)`).
* Reports display total elapsed time and are downloadable directly.

---

Link to the actual outputs: https://www.dropbox.com/scl/fo/agl251lobjpz87d7y2jfz/ADUyqFTfiJB0rckUNVkNtwc?rlkey=mrx7fi09qdo6ceebf8w3evvq5&dl=0

## 📄 License

ASU @ [Amar Yadav, Jinal Vyas]
