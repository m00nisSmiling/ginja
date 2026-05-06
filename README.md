# 👾 Ginja: GraphQL Ninja 👾

<img src="https://i.ibb.co/G3RmBkqm/ginja.jpg" width=300px height=150px>

Ginjaa is a Python-based security tool designed to interact with GraphQL endpoints. It performs introspection to map out the database schema and allows for automated data extraction into JSON or CSV formats.

## 🚀 Installation

1. **Clone the repository:**
```
git clone https://github.com/m00nisSmiling/ginja.git
cd ginja
```
2. **Install dependencies:**
```
pip install -r requirements.txt
```
3. **Run script using python**
```
python ginja.py
```
4. **Direct Arguments**
- You can skip the initial prompts by passing the domain and route as arguments:
```
python ginja.py example.com /v1/graphql
```
<hr>

## 💻 Once the tool is running, use the following queries:

- rdb: Extract and list the table schema.  
- rcol: Extract columns from a specific table and dump data.  
- all: Automatically dump the entire database schema.  
- csv: Toggle CSV export mode ON/OFF.  
- clear: Remove local caches/folders for the current session.  
- exit: Close the tool.

## 📂 Output Structure
- Ginja creates a directory named after the target domain. Inside, it organizes data by table name, saving results as table_name.json or table_name.csv
- Disclaimer: This tool is for educational and authorized security testing only.

## ⚙️ Technical Details Summary
- Connectivity: The script checks for http first and falls back to https if needed.  
- Data Handling: Automatically ignores metadata columns like created_at and updated_at to keep dumps clean.  
- Headers: Includes A feature to add custom headers (like Authorization tokens) during setup.  
- Format Protection: When exporting to CSV, it wraps long numbers in ="value" to prevent Excel from ruining the formatting[cite: 1].
