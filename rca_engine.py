"""rca_engine.py
Core logic for the Root Cause Analysis (RCA) tool: loading Excel data,
counting how often each category occurs, and drawing a ranked bar chart.

Kept separate from the GUI (main.py) so the logic can be tested and reused
without needing to open any window.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as _fm

# --- Korean font setup (prevents '글자 깨짐' / garbled Korean text in charts) ---
_PREFERRED_FONTS = ["Malgun Gothic", "AppleGothic", "NanumGothic", "Arial"]
_AVAILABLE = {f.name for f in _fm.fontManager.ttflist}
_FONT = next((f for f in _PREFERRED_FONTS if f in _AVAILABLE), "DejaVu Sans")
plt.rcParams["font.family"] = _FONT
plt.rcParams["axes.unicode_minus"] = False


def load_excel(path: str) -> pd.DataFrame:
    """Read an Excel file into a DataFrame. Raises on bad/missing file."""
    return pd.read_excel(path)


def count_categories(df: pd.DataFrame, category_col: str) -> pd.Series:
    """Count occurrences of each value in `category_col`, sorted descending
    (most frequent root cause first). Blank/NaN rows are ignored.
    """
    series = df[category_col].dropna().astype(str).str.strip()
    series = series[series != ""]
    return series.value_counts()  # already sorted descending by pandas


def draw_ranked_bar_chart(ax, counts: pd.Series, title: str = "Root Cause Ranking"):
    """Draw a horizontal ranked bar chart (most frequent cause at the top)."""
    if counts.empty:
        ax.text(0.5, 0.5, "표시할 데이터가 없습니다.\n(No data to display)",
                ha="center", va="center", color="gray")
        ax.set_xticks([])
        ax.set_yticks([])
        return

    # Reverse so the largest bar is drawn at the top of the horizontal chart.
    ordered = counts.iloc[::-1]
    ax.barh(ordered.index.astype(str), ordered.values, color="#4C72B0")
    ax.set_xlabel("건수 (Count)")
    ax.set_title(title, fontweight="bold")
    for i, v in enumerate(ordered.values):
        ax.text(v, i, f" {v}", va="center", fontsize=9)
