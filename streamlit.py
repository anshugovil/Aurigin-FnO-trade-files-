@staticmethod
    def get_futures_code(date_str: str) -> Tuple[Optional[str], Optional[str]]:
        """Get futures month and year code"""
        dt = DateUtils.parse_date(date_str)
        if not dt:
            return None, None
        return MONTH_CODE.get(dt.month), str(dt.year)[-1]
    
    @staticmethod
    def get_nifty_weekly_suffix(exp_dt: datetime) -> str:
        """Calculate NIFTY weekly option suffix"""
        cutoff = date(2025, 9, 1)
        target_wd = 3 if exp_dt.date() < cutoff else 1
        
        first_day = date(exp_dt.year, exp_dt.month, 1)
        _, ndays = calendar.monthrange(exp_dt.year, exp_dt.month)
        days = [first_day + timedelta(days=i) for i in range(ndays)]
        targets = [d for d in days if d.weekday() == target_wd]
        
        if not targets:
            return ""
        
        d0 = exp_dt.date()
        nearest = min(targets, key=lambda d: abs((d - d0).days))
        
        if nearest == targets[-1]:
            return ""
        
        ordinal = targets.index(nearest) + 1
        suffixes = {1: "C", 2: "D", 3: "E", 4: "F"}
        return suffixes.get(ordinal, "")

class TickerBuilder:
    """Build security tickers based on rules"""
    
    def __init__(self, futures_map: Dict[str, str]):
        self.futures_map = futures_map
        self.index_map = INDEX_OPTIONS_MAPPING
    
    def build_option_ticker(self, instrument: str, symbol: str, expiry: str, 
                           strike: str, option_type: str) -> str:
        """Build option ticker string"""
        exp_fmt = DateUtils.format_mmddyy(expiry)
        cp = self._get_cp_letter(option_type)
        
        strike = str(strike).replace(",", "").replace(r'\.0+#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit App for Aurigin Trade Transformer
Run with: streamlit run aurigin_streamlit.py
"""

import streamlit as st
import pandas as pd
import io
import sys
import re
import calendar
import requests
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple, Any
import warnings
import base64
warnings.filterwarnings('ignore')

# ====================
# STREAMLIT PAGE CONFIG
# ====================

st.set_page_config(
    page_title="Aurigin Trade Transformer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# GITHUB CONFIGURATION
# ====================

GITHUB_MAPPING_URL = "https://raw.githubusercontent.com/anshugovil/Aurigin-FnO-trade-files-/main/futures%20mapping.csv"

# ====================
# CONSTANTS
# ====================

EXCEL_PASSWORD = "Aurigin2017"

MONTH_CODE = {
    1: "F", 2: "G", 3: "H", 4: "J", 5: "K", 6: "M",
    7: "N", 8: "Q", 9: "U", 10: "V", 11: "X", 12: "Z"
}

INPUT_COLUMNS = {
    "tm_name": 3,        # Column 4: TM NAME
    "instrument": 4,     # Column 5: INSTR
    "symbol": 5,         # Column 6: Symbol
    "expiry": 6,         # Column 7: Expiry Date
    "strike": 8,         # Column 9: Strike Price
    "option_type": 9,    # Column 10: Option Type (CE/PE)
    "side": 10,          # Column 11: B/S (Buy/Sell)
    "quantity": 12,      # Column 13: QTY
    "price": 13          # Column 14: Avg Price
}

INDEX_OPTIONS_MAPPING = {
    "NIFTY": "NIFTY",
    "NSEBANK": "NSEBANK",
    "BANKNIFTY": "NSEBANK",
    "NMIDSELP": "NMIDSELP",
    "MIDCPNIFTY": "NMIDSELP",
    "FINNIFTY": "FINNIFTY",
    "NIFTYFIN": "FINNIFTY"
}

# Fallback mapping if GitHub fails
DEFAULT_FUTURES_MAPPING = {
    "NIFTY": "NIFTY",
    "BANKNIFTY": "NSEBANK",
    "FINNIFTY": "FINNIFTY",
    "MIDCPNIFTY": "NMIDSELP"
}

# ====================
# UTILITY CLASSES
# ====================

class DateUtils:
    """Date parsing and formatting utilities"""
    
    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """Parse date string to datetime"""
        s = str(date_str).strip().replace(".", "/").replace("-", "/")
        formats = [
            "%d/%m/%Y", "%d/%m/%y", "%m/%d/%Y", 
            "%m/%d/%y", "%Y/%m/%d", "%Y/%d/%m"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(s, fmt)
            except:
                continue
        
        try:
            dt = pd.to_datetime(s, dayfirst=True, errors="coerce")
            if not pd.isna(dt):
                return dt.to_pydatetime()
        except:
            pass
        
        return None
    
    @staticmethod
    def format_mmddyy(date_str: str) -> str:
        """Format date as MM/DD/YY"""
        dt = DateUtils.parse_date(date_str)
        return dt.strftime("%m/%d/%y") if dt else ""
    
    @staticmethod
    def format_yyyymmdd(date_str: str) -> str:
        """Format date as YYYYMMDD"""
        dt = DateUtils.parse_date(date_str)
        return dt.strftime("%Y%m%d") if dt else ""
    
    @staticmethod
    def get_futures_code(date_str: str) -> Tuple[Optional[str], Optional[str]]:
        """Get futures month and year code"""
        dt = DateUtils.parse_date(date_str)
        if not dt, '')
        
        if instrument == "OPTSTK":
            ticker = self.futures_map.get(symbol, "UPDATE")
            if ticker != "UPDATE" and exp_fmt and cp and strike:
                return f"{ticker} IS {exp_fmt} {cp}{strike} Equity"
        else:
            ticker = self.index_map.get(symbol, "")
            if ticker == "NIFTY":
                dt = DateUtils.parse_date(expiry)
                if dt:
                    suffix = DateUtils.get_nifty_weekly_suffix(dt)
                    ticker = f"{ticker}{suffix}"
            if ticker and exp_fmt and cp and strike:
                return f"{ticker} {exp_fmt} {cp}{strike} Index"
        
        return "UPDATE"
    
    def build_futures_ticker(self, instrument: str, symbol: str, expiry: str) -> str:
        """Build futures ticker string"""
        mcode, ycode = DateUtils.get_futures_code(expiry)
        ticker = self.futures_map.get(symbol, "UPDATE")
        
        if instrument == "FUTSTK":
            if ticker != "UPDATE" and mcode and ycode:
                return f"{ticker}={mcode}{ycode} IS Equity"
        else:
            if ticker != "UPDATE" and mcode and ycode:
                return f"{ticker}{mcode}{ycode} Index"
        
        return "UPDATE"
    
    def _get_cp_letter(self, option_type: str) -> str:
        """Get call/put letter"""
        s = str(option_type).upper().strip()
        if s in ("C", "CE", "CALL", "CALLS") or s.startswith("C"):
            return "C"
        if s in ("P", "PE", "PUT", "PUTS") or s.startswith("P") or "PE" in s:
            return "P"
        return ""

# ====================
# TRADE PROCESSOR
# ====================

def process_trades(df_input: pd.DataFrame, futures_map: Dict[str, str], trade_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Process input dataframe and return options and futures dataframes"""
    
    ticker_builder = TickerBuilder(futures_map)
    
    if 4 >= len(df_input.columns):
        raise ValueError("Input file doesn't have enough columns. Expected at least 14 columns.")
    
    instr_col = df_input.columns[4]
    instr_values = df_input[instr_col].astype(str).str.upper()
    
    options_mask = instr_values.isin(["OPTSTK", "OPTIDX"])
    df_options = df_input[options_mask].reset_index(drop=True)
    
    futures_mask = instr_values.isin(["FUTSTK", "FUTIDX"])
    df_futures = df_input[futures_mask].reset_index(drop=True)
    
    def extract_data(df):
        data = {}
        for key, col_idx in INPUT_COLUMNS.items():
            if col_idx < len(df.columns):
                data[key] = df.iloc[:, col_idx].astype(str)
            else:
                data[key] = pd.Series([""] * len(df))
        
        if "strike" in data:
            data["strike"] = data["strike"].str.replace(",", "", regex=False)
            data["strike"] = data["strike"].str.replace(r'\.0+#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit App for Aurigin Trade Transformer
Run with: streamlit run aurigin_streamlit.py
"""

import streamlit as st
import pandas as pd
import io
import sys
import re
import calendar
import requests
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple, Any
import warnings
import base64
warnings.filterwarnings('ignore')

# ====================
# STREAMLIT PAGE CONFIG
# ====================

st.set_page_config(
    page_title="Aurigin Trade Transformer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# GITHUB CONFIGURATION
# ====================

GITHUB_MAPPING_URL = "https://raw.githubusercontent.com/anshugovil/Aurigin-FnO-trade-files-/main/futures%20mapping.csv"

# ====================
# CONSTANTS
# ====================

EXCEL_PASSWORD = "Aurigin2017"

MONTH_CODE = {
    1: "F", 2: "G", 3: "H", 4: "J", 5: "K", 6: "M",
    7: "N", 8: "Q", 9: "U", 10: "V", 11: "X", 12: "Z"
}

INPUT_COLUMNS = {
    "tm_name": 3,        # Column 4: TM NAME
    "instrument": 4,     # Column 5: INSTR
    "symbol": 5,         # Column 6: Symbol
    "expiry": 6,         # Column 7: Expiry Date
    "strike": 8,         # Column 9: Strike Price
    "option_type": 9,    # Column 10: Option Type (CE/PE)
    "side": 10,          # Column 11: B/S (Buy/Sell)
    "quantity": 12,      # Column 13: QTY
    "price": 13          # Column 14: Avg Price
}

INDEX_OPTIONS_MAPPING = {
    "NIFTY": "NIFTY",
    "NSEBANK": "NSEBANK",
    "BANKNIFTY": "NSEBANK",
    "NMIDSELP": "NMIDSELP",
    "MIDCPNIFTY": "NMIDSELP",
    "FINNIFTY": "FINNIFTY",
    "NIFTYFIN": "FINNIFTY"
}

# Fallback mapping if GitHub fails
DEFAULT_FUTURES_MAPPING = {
    "NIFTY": "NIFTY",
    "BANKNIFTY": "NSEBANK",
    "FINNIFTY": "FINNIFTY",
    "MIDCPNIFTY": "NMIDSELP"
}

# ====================
# UTILITY CLASSES
# ====================

class DateUtils:
    """Date parsing and formatting utilities"""
    
    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """Parse date string to datetime"""
        s = str(date_str).strip().replace(".", "/").replace("-", "/")
        formats = [
            "%d/%m/%Y", "%d/%m/%y", "%m/%d/%Y", 
            "%m/%d/%y", "%Y/%m/%d", "%Y/%d/%m"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(s, fmt)
            except:
                continue
        
        try:
            dt = pd.to_datetime(s, dayfirst=True, errors="coerce")
            if not pd.isna(dt):
                return dt.to_pydatetime()
        except:
            pass
        
        return None
    
    @staticmethod
    def format_mmddyy(date_str: str) -> str:
        """Format date as MM/DD/YY"""
        dt = DateUtils.parse_date(date_str)
        return dt.strftime("%m/%d/%y") if dt else ""
    
    @staticmethod
    def format_yyyymmdd(date_str: str) -> str:
        """Format date as YYYYMMDD"""
        dt = DateUtils.parse_date(date_str)
        return dt.strftime("%Y%m%d") if dt else ""
    
    @staticmethod
    def get_futures_code(date_str: str) -> Tuple[Optional[str], Optional[str]]:
        """Get futures month and year code"""
        dt = DateUtils.parse_date(date_str)
        if not dt, '', regex=True)
        
        return data
    
    # Build OPTIONS output
    out_options = pd.DataFrame()
    if len(df_options) > 0:
        input_data = extract_data(df_options)
        n = len(df_options)
        
        out_options["RequestType"] = "NEW"
        out_options["ExternalReference"] = "PLEASE FILL"
        out_options["RevisionNumber"] = "1"
        
        tickers = []
        for i in range(n):
            instrument = input_data["instrument"].iat[i]
            symbol = input_data["symbol"].iat[i]
            expiry = input_data["expiry"].iat[i]
            strike = input_data["strike"].iat[i]
            opt_type = input_data["option_type"].iat[i]
            ticker = ticker_builder.build_option_ticker(
                instrument, symbol, expiry, strike, opt_type
            )
            tickers.append(ticker)
        out_options["SecurityIdentifier"] = tickers
        
        side = input_data["side"]
        out_options["ActionCode"] = ["B" if s.upper().startswith("B") else "S" for s in side]
        out_options["Quantity"] = input_data["quantity"]
        out_options["Price"] = input_data["price"]
        out_options["TradeDate"] = trade_date
        out_options["SettlementDate"] = trade_date
        out_options["SettlementCurrency"] = "INR"
        out_options["SettlementRate"] = "1"
        out_options["Tax"] = ""
        out_options["Commission"] = "0"
        out_options["OtherFee"] = "0"
        out_options["Memo"] = ""
        out_options["LegalEntity"] = "AUM01"
        out_options["Counterparty"] = input_data["tm_name"]
        out_options["OptionClearer"] = "GS India Futures"
        out_options["OptionClearerAccount"] = "OOI93890"
        
        strategy = []
        opt_type = input_data["option_type"]
        for i in range(n):
            s = side.iat[i].upper().strip()
            t = opt_type.iat[i].upper().strip()
            
            if s.startswith("B") and (t in ("CE", "C") or t.startswith("C")):
                strategy.append("FULO")
            elif s.startswith("S") and (t in ("CE", "C") or t.startswith("C")):
                strategy.append("FUSH")
            elif s.startswith("B") and (t in ("PE", "P") or t.startswith("P") or "PE" in t):
                strategy.append("FUSH")
            elif s.startswith("S") and (t in ("PE", "P") or t.startswith("P") or "PE" in t):
                strategy.append("FUSH")
            else:
                strategy.append("FULO")
        out_options["Strategy"] = strategy
        
        out_options["FundStructure"] = ""
        out_options["Trader"] = "Anurag Gupta"
        for i in range(1, 6):
            out_options[f"TBD{i}"] = ""
        for i in range(1, 6):
            out_options[f"UserDefined{i}"] = ""
    
    # Build FUTURES output
    out_futures = pd.DataFrame()
    if len(df_futures) > 0:
        input_data = extract_data(df_futures)
        n = len(df_futures)
        
        out_futures["RequestType"] = "NEW"
        out_futures["ExternalReference"] = "PLEASE FILL"
        out_futures["RevisionNumber"] = "1"
        
        side = input_data["side"]
        out_futures["ActionCode"] = ["B" if s.upper().startswith("B") else "S" for s in side]
        
        tickers = []
        for i in range(n):
            instrument = input_data["instrument"].iat[i]
            symbol = input_data["symbol"].iat[i]
            expiry = input_data["expiry"].iat[i]
            ticker = ticker_builder.build_futures_ticker(instrument, symbol, expiry)
            tickers.append(ticker)
        out_futures["SecurityIdentifier"] = tickers
        
        out_futures["Quantity"] = input_data["quantity"]
        out_futures["Price"] = input_data["price"]
        out_futures["TradeDate"] = trade_date
        out_futures["SettlementCurrency"] = "INR"
        out_futures["SettlementRate"] = ""
        out_futures["Commission"] = ""
        out_futures["OtherFee"] = ""
        out_futures["Memo"] = ""
        out_futures["LegalEntity"] = "AUM01"
        out_futures["Counterparty"] = input_data["tm_name"]
        out_futures["Strategy"] = ["FULO" if s.upper().startswith("B") else "FUSH" for s in side]
        out_futures["FuturesClearer"] = "GS India Futures"
        out_futures["FuturesClearerAccount"] = "OOI93890"
        out_futures["FundStructure"] = ""
        out_futures["Trader"] = "Anurag Gupta"
        out_futures["Exchange"] = ""
        out_futures["ProductType"] = ""
        for i in range(1, 6):
            out_futures[f"TBD{i}"] = ""
        for i in range(1, 6):
            out_futures[f"UserDefined{i}"] = ""
    
    return out_options, out_futures

def get_download_link(df: pd.DataFrame, filename: str) -> str:
    """Generate a download link for a dataframe"""
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download {filename}</a>'

def load_futures_mapping_from_github(url: str) -> Dict[str, str]:
    """Load futures mapping from GitHub"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        mapping_df = pd.read_csv(io.StringIO(response.text), dtype=str).fillna("")
        futures_map = {}
        for _, row in mapping_df.iterrows():
            symbol = str(row.iloc[0]).strip().upper()
            ticker = str(row.iloc[1]).strip().upper() or "UPDATE"
            if symbol:
                futures_map[symbol] = ticker
        return futures_map
    except Exception as e:
        st.warning(f"Could not load mapping from GitHub: {e}")
        st.info("Using fallback default mapping")
        return DEFAULT_FUTURES_MAPPING.copy()

# ====================
# STREAMLIT APP
# ====================

def main():
    st.title("🚀 Aurigin Trade Transformer")
    st.markdown("### Transform GS trade files into Aurigin format")
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("📅 Trade Date")
        use_today = st.checkbox("Use today's date", value=True)
        if use_today:
            trade_date = datetime.now().strftime("%Y%m%d")
            st.info(f"Trade Date: {trade_date}")
        else:
            trade_date_input = st.date_input("Select trade date")
            trade_date = trade_date_input.strftime("%Y%m%d")
        
        st.subheader("📊 Futures Mapping")
        
        if 'futures_map' not in st.session_state:
            with st.spinner("Loading mapping from GitHub..."):
                st.session_state.futures_map = load_futures_mapping_from_github(GITHUB_MAPPING_URL)
                st.success(f"✓ Loaded {len(st.session_state.futures_map)} mappings from GitHub")
        
        futures_map = st.session_state.futures_map.copy()
        
        st.markdown("---")
        override_mapping = st.checkbox("Override with custom mapping file")
        
        if override_mapping:
            mapping_file = st.file_uploader(
                "Upload custom futures mapping CSV",
                type=['csv'],
                help="CSV file with 2 columns: Symbol, Bloomberg Ticker"
            )
            if mapping_file:
                try:
                    mapping_df = pd.read_csv(mapping_file, dtype=str).fillna("")
                    custom_map = {}
                    for _, row in mapping_df.iterrows():
                        symbol = str(row.iloc[0]).strip().upper()
                        ticker = str(row.iloc[1]).strip().upper() or "UPDATE"
                        if symbol:
                            custom_map[symbol] = ticker
                    futures_map = custom_map
                    st.success(f"✓ Using custom mapping ({len(futures_map)} symbols)")
                except Exception as e:
                    st.error(f"Error loading mapping: {e}")
                    st.info("Continuing with GitHub mapping")
        
        if st.button("🔄 Reload from GitHub"):
            with st.spinner("Reloading..."):
                st.session_state.futures_map = load_futures_mapping_from_github(GITHUB_MAPPING_URL)
                futures_map = st.session_state.futures_map.copy()
                st.success(f"✓ Reloaded {len(futures_map)} mappings from GitHub")
                st.rerun()
        
        with st.expander("View Current Mapping"):
            source = "Custom Upload" if override_mapping and mapping_file else "GitHub"
            st.write(f"**Source:** {source}")
            st.write(f"**Total mappings:** {len(futures_map)}")
            
            search_term = st.text_input("Search symbol", "")
            
            if search_term:
                filtered = {k: v for k, v in futures_map.items() 
                          if search_term.upper() in k or search_term.upper() in v}
                if filtered:
                    st.write(f"Found {len(filtered)} matches:")
                    for symbol, ticker in filtered.items():
                        st.text(f"{symbol} → {ticker}")
                else:
                    st.write("No matches found")
            else:
                sample_mappings = list(futures_map.items())[:10]
                for symbol, ticker in sample_mappings:
                    st.text(f"{symbol} → {ticker}")
                if len(futures_map) > 10:
                    st.text(f"... and {len(futures_map) - 10} more")
    
    st.header("📁 Upload Trade File")
    
    uploaded_file = st.file_uploader(
        "Choose your GS trade file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload the trade file (CSV or Excel format)"
    )
    
    if uploaded_file:
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                df_input = pd.read_csv(uploaded_file, dtype=str).fillna("")
            else:
                try:
                    df_input = pd.read_excel(
                        uploaded_file, 
                        dtype=str,
                        engine='openpyxl' if file_extension == 'xlsx' else 'xlrd'
                    ).fillna("")
                except:
                    df_input = pd.read_excel(uploaded_file, dtype=str).fillna("")
            
            st.subheader("📊 Input File Preview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", len(df_input))
            with col2:
                st.metric("Total Columns", len(df_input.columns))
            
            if 4 < len(df_input.columns):
                instr_col = df_input.columns[4]
                instr_values = df_input[instr_col].astype(str).str.upper()
                options_count = instr_values.isin(["OPTSTK", "OPTIDX"]).sum()
                futures_count = instr_values.isin(["FUTSTK", "FUTIDX"]).sum()
                
                with col3:
                    st.metric("Options", options_count)
                    st.metric("Futures", futures_count)
            
            with st.expander("View Input Data"):
                st.dataframe(df_input.head(20))
            
            if st.button("🔄 Transform Data", type="primary"):
                with st.spinner("Processing trades..."):
                    try:
                        options_df, futures_df = process_trades(df_input, futures_map, trade_date)
                        
                        st.success("✅ Transformation Complete!")
                        
                        tab1, tab2 = st.tabs(["📈 Options Output", "📊 Futures Output"])
                        
                        with tab1:
                            if len(options_df) > 0:
                                st.subheader(f"Options Trades ({len(options_df)} rows)")
                                st.dataframe(options_df.head(20))
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = f"aurigin_option_trades_{timestamp}.csv"
                                st.markdown(get_download_link(options_df, filename), unsafe_allow_html=True)
                                
                                with st.expander("Options Statistics"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write("**Action Code Distribution:**")
                                        st.write(options_df["ActionCode"].value_counts())
                                    with col2:
                                        st.write("**Strategy Distribution:**")
                                        st.write(options_df["Strategy"].value_counts())
                            else:
                                st.info("No option trades found in the input file")
                        
                        with tab2:
                            if len(futures_df) > 0:
                                st.subheader(f"Futures Trades ({len(futures_df)} rows)")
                                st.dataframe(futures_df.head(20))
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = f"aurigin_futures_trades_{timestamp}.csv"
                                st.markdown(get_download_link(futures_df, filename), unsafe_allow_html=True)
                                
                                with st.expander("Futures Statistics"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write("**Action Code Distribution:**")
                                        st.write(futures_df["ActionCode"].value_counts())
                                    with col2:
                                        st.write("**Strategy Distribution:**")
                                        st.write(futures_df["Strategy"].value_counts())
                            else:
                                st.info("No futures trades found in the input file")
                        
                        all_tickers = []
                        if len(options_df) > 0:
                            all_tickers.extend(options_df["SecurityIdentifier"].tolist())
                        if len(futures_df) > 0:
                            all_tickers.extend(futures_df["SecurityIdentifier"].tolist())
                        
                        update_needed = [t for t in all_tickers if "UPDATE" in t]
                        if update_needed:
                            st.warning(f"⚠️ {len(update_needed)} tickers need mapping updates")
                            with st.expander("Show tickers needing update"):
                                for ticker in set(update_needed):
                                    st.text(ticker)
                    
                    except Exception as e:
                        st.error(f"Error processing file: {str(e)}")
                        st.exception(e)
        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.info("Make sure the file is a valid CSV or Excel file with the expected format")
    
    with st.expander("📖 Instructions"):
        st.markdown("""
        ### How to use:
        1. **Trade Date**: Set in sidebar (default is today)
        2. **Upload File**: Upload your GS trade file (CSV/Excel)
        3. **Transform**: Click "Transform Data" button
        4. **Download**: Download the transformed CSV files
        
        ### Mapping:
        - Automatically loads from GitHub repository
        - Option to override with custom file
        - Search symbols in the mapping viewer
        
        ### GitHub Repository:
        - User: anshugovil
        - Repo: Aurigin-FnO-trade-files-
        - File: futures mapping.csv
        """)
    
    st.markdown("---")
    st.markdown("**Aurigin Trade Transformer** | GitHub: anshugovil/Aurigin-FnO-trade-files-")

if __name__ == "__main__":
    main()#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit App for Aurigin Trade Transformer
Run with: streamlit run aurigin_streamlit.py
"""

import streamlit as st
import pandas as pd
import io
import sys
import re
import calendar
import requests
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple, Any
import warnings
import base64
warnings.filterwarnings('ignore')

# ====================
# STREAMLIT PAGE CONFIG
# ====================

st.set_page_config(
    page_title="Aurigin Trade Transformer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# GITHUB CONFIGURATION
# ====================

GITHUB_MAPPING_URL = "https://raw.githubusercontent.com/anshugovil/Aurigin-FnO-trade-files-/main/futures%20mapping.csv"

# ====================
# CONSTANTS
# ====================

EXCEL_PASSWORD = "Aurigin2017"

MONTH_CODE = {
    1: "F", 2: "G", 3: "H", 4: "J", 5: "K", 6: "M",
    7: "N", 8: "Q", 9: "U", 10: "V", 11: "X", 12: "Z"
}

INPUT_COLUMNS = {
    "tm_name": 3,        # Column 4: TM NAME
    "instrument": 4,     # Column 5: INSTR
    "symbol": 5,         # Column 6: Symbol
    "expiry": 6,         # Column 7: Expiry Date
    "strike": 8,         # Column 9: Strike Price
    "option_type": 9,    # Column 10: Option Type (CE/PE)
    "side": 10,          # Column 11: B/S (Buy/Sell)
    "quantity": 12,      # Column 13: QTY
    "price": 13          # Column 14: Avg Price
}

INDEX_OPTIONS_MAPPING = {
    "NIFTY": "NIFTY",
    "NSEBANK": "NSEBANK",
    "BANKNIFTY": "NSEBANK",
    "NMIDSELP": "NMIDSELP",
    "MIDCPNIFTY": "NMIDSELP",
    "FINNIFTY": "FINNIFTY",
    "NIFTYFIN": "FINNIFTY"
}

# Fallback mapping if GitHub fails
DEFAULT_FUTURES_MAPPING = {
    "NIFTY": "NIFTY",
    "BANKNIFTY": "NSEBANK",
    "FINNIFTY": "FINNIFTY",
    "MIDCPNIFTY": "NMIDSELP"
}

# ====================
# UTILITY CLASSES
# ====================

class DateUtils:
    """Date parsing and formatting utilities"""
    
    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """Parse date string to datetime"""
        s = str(date_str).strip().replace(".", "/").replace("-", "/")
        formats = [
            "%d/%m/%Y", "%d/%m/%y", "%m/%d/%Y", 
            "%m/%d/%y", "%Y/%m/%d", "%Y/%d/%m"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(s, fmt)
            except:
                continue
        
        try:
            dt = pd.to_datetime(s, dayfirst=True, errors="coerce")
            if not pd.isna(dt):
                return dt.to_pydatetime()
        except:
            pass
        
        return None
    
    @staticmethod
    def format_mmddyy(date_str: str) -> str:
        """Format date as MM/DD/YY"""
        dt = DateUtils.parse_date(date_str)
        return dt.strftime("%m/%d/%y") if dt else ""
    
    @staticmethod
    def format_yyyymmdd(date_str: str) -> str:
        """Format date as YYYYMMDD"""
        dt = DateUtils.parse_date(date_str)
        return dt.strftime("%Y%m%d") if dt else ""
    
    @staticmethod
    def get_futures_code(date_str: str) -> Tuple[Optional[str], Optional[str]]:
        """Get futures month and year code"""
        dt = DateUtils.parse_date(date_str)
        if not dt
