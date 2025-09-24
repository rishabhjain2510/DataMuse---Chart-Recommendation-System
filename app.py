import os
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend for web servers
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request, redirect, url_for

# --- App Configuration ---
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["CHART_FOLDER"] = "static/charts"

# --- Ensure Folders Exist ---
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["CHART_FOLDER"], exist_ok=True)

df = None  # Global dataframe - suitable only for single-user context

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def upload_file():
    """Handles file upload and reads it into the global dataframe."""
    global df
    if request.method == "POST":
        # Check if file part exists in the request
        if 'file' not in request.files:
            return render_template("upload.html", error="No file selected. Please choose a file to upload.")
        
        file = request.files['file']
        
        # Check if a file was actually selected
        if file.filename == '' or file.filename is None:
            return render_template("upload.html", error="No file selected. Please choose a file to upload.")
            
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            try:
                if file.filename.lower().endswith(".csv"):
                    df = pd.read_csv(filepath)
                elif file.filename.lower().endswith((".xlsx", ".xls")):
                    df = pd.read_excel(filepath)
                else:
                    return render_template("upload.html", error="Unsupported file format. Please upload a CSV or Excel file.")
                
                # --- NEW: Attempt to convert object columns to datetime ---
                for col in df.columns:
                    if df[col].dtype == 'object':
                        try:
                            df[col] = pd.to_datetime(df[col], errors='ignore')
                        except (ValueError, TypeError):
                            pass # Column is not a datetime, leave as object
            
            except Exception as e:
                 return render_template("upload.html", error=f"Error reading file: {e}")

            return redirect(url_for("generate_chart"))
            
    return render_template("upload.html")

@app.route("/generate_chart", methods=["GET", "POST"])
@app.route("/choose_chart", methods=["GET", "POST"])  # Backward compatibility
def generate_chart():
    """Allows user to select columns and generates a chart based on smart rules."""
    global df
    if df is None:
        return redirect(url_for("upload_file"))

    # Identify column types, now including datetime
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

    chart_url = None
    if request.method == "POST":
        chart_type = request.form["chart_type"]
        col1 = request.form.get("col1")
        col2 = request.form.get("col2")
        rotation = int(request.form.get("rotation", 0))
        y_rotation = int(request.form.get("y_rotation", 0))

        # Ensure selected columns exist in dataframe to prevent errors
        if (col1 and col1 not in df.columns) or (col2 and col2 not in df.columns):
            return "Error: Invalid column selected.", 400

        chart_filename = "chart.png" # Static filename
        chart_path = os.path.join(app.config["CHART_FOLDER"], chart_filename)

        plt.figure(figsize=(14, 10))
        sns.set_theme(style="whitegrid")
        
        # Chart generation logic
        if chart_type == "Histogram":
            sns.histplot(df[col1], kde=True)
            plt.title(f"Distribution of {col1}", fontsize=20, pad=20)
        elif chart_type == "Box Plot (Single Column)":
             sns.boxplot(y=df[col1])
             plt.title(f"Box Plot of {col1}", fontsize=20, pad=20)
        elif chart_type == "Count Plot":
            sns.countplot(x=df[col1], order=df[col1].value_counts().index)
            plt.title(f"Frequency of Categories in {col1}", fontsize=20, pad=20)
        elif chart_type == "Pie Chart":
            df[col1].value_counts().plot(kind="pie", autopct="%1.1f%%", startangle=140, fontsize=14)
            plt.ylabel("")
            plt.title(f"Proportion of Categories in {col1}", fontsize=20, pad=20)
        elif chart_type == "Scatter Plot":
            sns.scatterplot(data=df, x=col1, y=col2)
            plt.title(f"Scatter Plot: {col1} vs {col2}", fontsize=20, pad=20)
        elif chart_type == "Line Plot (Time-Series)":
            # Ensure the datetime column is on the x-axis
            x_col, y_col = (col1, col2) if col1 in datetime_cols else (col2, col1)
            sns.lineplot(data=df, x=x_col, y=y_col)
            plt.title(f"Trend of {y_col} over Time", fontsize=20, pad=20)
        elif chart_type == "Bar Plot (by Value)":
            # Ensure the categorical column is on the x-axis
            x_col, y_col = (col1, col2) if col1 in categorical_cols else (col2, col1)
            sns.barplot(data=df, x=x_col, y=y_col, estimator=sum)
            plt.title(f"Total {y_col} by {x_col}", fontsize=20, pad=20)
        elif chart_type == "Box Plot (by Category)":
            x_col, y_col = (col1, col2) if col1 in categorical_cols else (col2, col1)
            sns.boxplot(data=df, x=x_col, y=y_col)
            plt.title(f"Distribution of {y_col} across {x_col}", fontsize=20, pad=20)
        elif chart_type == "Correlation Heatmap":
            numeric_df = df.select_dtypes(include=["number"])
            corr = numeric_df.corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={'fontsize': 12})
            plt.title("Correlation Heatmap of Numeric Columns", fontsize=20, pad=20)
        
        plt.xticks(rotation=rotation, fontsize=12)
        plt.yticks(rotation=y_rotation, fontsize=12)
        plt.xlabel(plt.gca().get_xlabel(), fontsize=14)
        plt.ylabel(plt.gca().get_ylabel(), fontsize=14)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=200, bbox_inches='tight')
        plt.close()

        chart_url = url_for('static', filename=f'charts/{chart_filename}')

    # Pass all column types to the template along with chart_url
    return render_template("generate_chart.html",
                           all_cols=df.columns.tolist(),
                           numeric_cols=numeric_cols,
                           categorical_cols=categorical_cols,
                           datetime_cols=datetime_cols,
                           chart_url=chart_url)

@app.route("/generate_chart_ajax", methods=["POST"])
def generate_chart_ajax():
    """AJAX endpoint for generating charts without page refresh."""
    global df
    if df is None:
        return {"error": "No data loaded"}, 400

    from flask import jsonify
    
    # Identify column types
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

    try:
        chart_type = request.json["chart_type"]
        col1 = request.json.get("col1")
        col2 = request.json.get("col2")
        rotation = int(request.json.get("rotation", 0))
        y_rotation = int(request.json.get("y_rotation", 0))

        # Ensure selected columns exist in dataframe
        if (col1 and col1 not in df.columns) or (col2 and col2 not in df.columns):
            return jsonify({"error": "Invalid column selected"}), 400

        chart_filename = "chart.png"
        chart_path = os.path.join(app.config["CHART_FOLDER"], chart_filename)

        plt.figure(figsize=(14, 10))
        sns.set_theme(style="whitegrid")
        
        # Chart generation logic (same as above)
        if chart_type == "Histogram":
            sns.histplot(df[col1], kde=True)
            plt.title(f"Distribution of {col1}", fontsize=20, pad=20)
        elif chart_type == "Box Plot (Single Column)":
             sns.boxplot(y=df[col1])
             plt.title(f"Box Plot of {col1}", fontsize=20, pad=20)
        elif chart_type == "Count Plot":
            sns.countplot(x=df[col1], order=df[col1].value_counts().index)
            plt.title(f"Frequency of Categories in {col1}", fontsize=20, pad=20)
        elif chart_type == "Pie Chart":
            df[col1].value_counts().plot(kind="pie", autopct="%1.1f%%", startangle=140, fontsize=14)
            plt.ylabel("")
            plt.title(f"Proportion of Categories in {col1}", fontsize=20, pad=20)
        elif chart_type == "Scatter Plot":
            sns.scatterplot(data=df, x=col1, y=col2)
            plt.title(f"Scatter Plot: {col1} vs {col2}", fontsize=20, pad=20)
        elif chart_type == "Line Plot (Time-Series)":
            x_col, y_col = (col1, col2) if col1 in datetime_cols else (col2, col1)
            sns.lineplot(data=df, x=x_col, y=y_col)
            plt.title(f"Trend of {y_col} over Time", fontsize=20, pad=20)
        elif chart_type == "Bar Plot (by Value)":
            x_col, y_col = (col1, col2) if col1 in categorical_cols else (col2, col1)
            sns.barplot(data=df, x=x_col, y=y_col, estimator=sum)
            plt.title(f"Total {y_col} by {x_col}", fontsize=20, pad=20)
        elif chart_type == "Box Plot (by Category)":
            x_col, y_col = (col1, col2) if col1 in categorical_cols else (col2, col1)
            sns.boxplot(data=df, x=x_col, y=y_col)
            plt.title(f"Distribution of {y_col} across {x_col}", fontsize=20, pad=20)
        elif chart_type == "Correlation Heatmap":
            numeric_df = df.select_dtypes(include=["number"])
            corr = numeric_df.corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={'fontsize': 12})
            plt.title("Correlation Heatmap of Numeric Columns", fontsize=20, pad=20)
        
        plt.xticks(rotation=rotation, fontsize=12)
        plt.yticks(rotation=y_rotation, fontsize=12)
        plt.xlabel(plt.gca().get_xlabel(), fontsize=14)
        plt.ylabel(plt.gca().get_ylabel(), fontsize=14)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=200, bbox_inches='tight')
        plt.close()

        chart_url = url_for('static', filename=f'charts/{chart_filename}')
        return jsonify({"chart_url": chart_url, "success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, port=5000, host='0.0.0.0')

