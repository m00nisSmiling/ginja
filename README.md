# Ginja: GraphQL Introspection & Data Dumper

Ginja is a Python-based security tool designed to interact with GraphQL endpoints. It performs introspection to map out the database schema and allows for automated data extraction into JSON or CSV formats.

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
#### You can skip the initial prompts by passing the domain and route as arguments:
```
python ginja.py example.com /v1/graphql
```
<hr>

## Commands inside the tool

#### Once the tool is running, use the following queries:

- rdb: Extract and list the table schema.  
- rcol: Extract columns from a specific table and dump data.  
- all: Automatically dump the entire database schema.  
- csv: Toggle CSV export mode ON/OFF.  
- clear: Remove local caches/folders for the current session.  
- exit: Close the tool.
