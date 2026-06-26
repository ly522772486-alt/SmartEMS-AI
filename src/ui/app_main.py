import base64
import os
import uuid

import streamlit as st

from src.ui.services import (
    APP_TITLE,
    FEATURE_COLUMNS,
    PROJECT_ROOT,
    build_feature_dataset,
    build_multi_day_dataset,
    get_file_status,
    list_raw_excel_files,
    load_csv,
    load_prediction_files,
    preview_excel_file,
    run_strategy_backtest,
    train_price_model,
)


ASSET_DIR = PROJECT_ROOT / "assets" / "ui"
HERO_IMAGE = ASSET_DIR / "energy-hero.png"
WORKFLOW_IMAGE = ASSET_DIR / "ai-workflow.png"
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "123456"
AUTH_FLOW_VERSION = "login-v3"
APP_BOOT_ID = uuid.uuid4().hex


def image_data_url(path):
    if not path.exists():
        return ""
    suffix = path.suffix.lower().replace(".", "")
    mime = "jpeg" if suffix in {"jpg", "jpeg"} else suffix
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/{mime};base64,{encoded}"


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --ems-bg: #f4f7f9;
            --ems-panel: #ffffff;
            --ems-text: #172026;
            --ems-muted: #62717a;
            --ems-line: #d9e3e6;
            --ems-teal: #0f8f8c;
            --ems-dark: #0d2029;
        }
        .stApp {
            background: linear-gradient(180deg, #eef5f6 0%, #f8fafb 34%, #f4f7f9 100%);
            color: var(--ems-text);
        }
        [data-testid="stSidebar"] {
            background: #10232c;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        [data-testid="stSidebar"] * {
            color: rgba(255, 255, 255, 0.92);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label {
            padding: 8px 10px;
            border-radius: 8px;
            margin: 3px 0;
        }
        [data-testid="stHeader"] {
            background: rgba(244, 247, 249, 0.82);
            backdrop-filter: blur(10px);
        }
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 3rem;
            max-width: 1360px;
        }
        h1, h2, h3 {
            color: var(--ems-text);
            letter-spacing: 0;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: .35rem;
        }
        h2 {
            font-size: 1.35rem;
            margin-top: 1.25rem;
        }
        h3 {
            font-size: 1.05rem;
        }
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid var(--ems-line);
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 10px 24px rgba(18, 42, 52, 0.06);
        }
        div[data-testid="stMetricLabel"] p {
            color: var(--ems-muted);
            font-size: .82rem;
        }
        div[data-testid="stMetricValue"] {
            color: var(--ems-dark);
        }
        .stButton > button,
        .stDownloadButton > button {
            border-radius: 8px;
            border: 1px solid #0f8f8c;
            box-shadow: 0 8px 18px rgba(15, 143, 140, 0.14);
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #0f8f8c, #147b9f);
        }
        .ems-hero {
            min-height: 300px;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.18);
            background-size: cover;
            background-position: center;
            margin-bottom: 1.25rem;
            box-shadow: 0 18px 44px rgba(12, 29, 38, 0.16);
        }
        .ems-hero-inner {
            min-height: 300px;
            padding: 34px 38px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            background: linear-gradient(90deg, rgba(10, 30, 38, .90) 0%, rgba(10, 30, 38, .64) 40%, rgba(10, 30, 38, .08) 100%);
        }
        .ems-kicker {
            color: #74dbe4;
            font-size: .84rem;
            font-weight: 700;
            letter-spacing: .06em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .ems-hero-title {
            color: #fff;
            font-size: 2.25rem;
            line-height: 1.15;
            font-weight: 760;
            max-width: 650px;
            margin: 0 0 12px;
        }
        .ems-hero-copy {
            color: rgba(255, 255, 255, .82);
            max-width: 680px;
            font-size: 1rem;
            line-height: 1.7;
        }
        .ems-page-title {
            border-left: 4px solid var(--ems-teal);
            padding: 2px 0 2px 14px;
            margin: 0 0 18px;
        }
        .ems-page-title p {
            color: var(--ems-muted);
            margin: 4px 0 0;
        }
        .ems-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin: 16px 0 22px;
        }
        .ems-card {
            background: rgba(255,255,255,.94);
            border: 1px solid var(--ems-line);
            border-radius: 8px;
            padding: 16px 16px 15px;
            box-shadow: 0 10px 26px rgba(18, 42, 52, 0.06);
        }
        .ems-card-title {
            color: var(--ems-dark);
            font-weight: 720;
            margin-bottom: 6px;
        }
        .ems-card-copy {
            color: var(--ems-muted);
            font-size: .92rem;
            line-height: 1.55;
        }
        .ems-status {
            display: inline-flex;
            padding: 6px 10px;
            border-radius: 999px;
            background: #e8f7f6;
            color: #0b6f6c;
            border: 1px solid #bde8e5;
            font-size: .82rem;
            font-weight: 650;
        }
        .ems-image-frame img {
            border-radius: 8px;
            border: 1px solid var(--ems-line);
            box-shadow: 0 12px 30px rgba(18, 42, 52, 0.08);
        }
        .ems-login-shell {
            min-height: 74vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .ems-login-card {
            width: min(460px, 92vw);
            padding: 30px;
            border-radius: 8px;
            background: rgba(255,255,255,.96);
            border: 1px solid var(--ems-line);
            box-shadow: 0 22px 60px rgba(12, 29, 38, 0.16);
        }
        .ems-login-title {
            font-size: 1.6rem;
            font-weight: 760;
            color: var(--ems-dark);
            margin-bottom: 8px;
        }
        .ems-login-copy {
            color: var(--ems-muted);
            line-height: 1.6;
            margin-bottom: 18px;
        }
        .ems-login-bg {
            border-radius: 8px;
            padding: 1px;
            background-size: cover;
            background-position: center;
            box-shadow: 0 18px 44px rgba(12, 29, 38, 0.14);
        }
        .ems-login-mask {
            border-radius: 8px;
            background: linear-gradient(90deg, rgba(9, 26, 34, .62), rgba(9, 26, 34, .12));
            padding: 28px;
        }
        @media (max-width: 900px) {
            .ems-grid { grid-template-columns: 1fr; }
            .ems-hero-title { font-size: 1.65rem; }
            .ems-hero-inner { padding: 24px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_metric_row(metrics):
    columns = st.columns(len(metrics))
    for column, item in zip(columns, metrics):
        column.metric(item["label"], item["value"], item.get("delta"))


def render_page_title(title, subtitle):
    st.markdown(
        f"""
        <div class="ems-page-title">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    image_url = image_data_url(HERO_IMAGE)
    st.markdown(
        f"""
        <div class="ems-hero" style="background-image: url('{image_url}');">
            <div class="ems-hero-inner">
                <div class="ems-kicker">SmartEMS-AI</div>
                <div class="ems-hero-title">智能能源管理电价预测与调度优化平台</div>
                <div class="ems-hero-copy">
                    面向电力市场和储能 EMS 场景，覆盖数据治理、特征工程、机器学习预测、调度策略回测和经营报表分析。
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_capability_grid():
    st.markdown(
        """
        <div class="ems-grid">
            <div class="ems-card">
                <div class="ems-card-title">数据治理</div>
                <div class="ems-card-copy">统一管理原始 Excel、基础数据集和特征数据集，形成可复用的数据处理链路。</div>
            </div>
            <div class="ems-card">
                <div class="ems-card-title">价格预测</div>
                <div class="ems-card-copy">支持 RandomForest、LightGBM、XGBoost 等模型训练，输出 MAE、RMSE 和预测曲线。</div>
            </div>
            <div class="ems-card">
                <div class="ems-card-title">策略回测</div>
                <div class="ems-card-copy">按预测电价生成目标出力，结合爬坡和功率边界约束计算收益、成本和利润。</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_auth_credentials():
    username = os.environ.get("SMARTEMS_USERNAME") or DEMO_USERNAME
    password = os.environ.get("SMARTEMS_PASSWORD") or DEMO_PASSWORD
    return username, password


def is_login_configured():
    username, password = get_auth_credentials()
    return bool(username and password)


def verify_login(username, password):
    configured_username, configured_password = get_auth_credentials()
    return username == configured_username and password == configured_password


def render_login():
    image_url = image_data_url(HERO_IMAGE)
    left, center, right = st.columns([1, 1.05, 1])

    with center:
        st.markdown(
            f"""
            <div class="ems-login-bg" style="background-image: url('{image_url}');">
                <div class="ems-login-mask">
                    <div class="ems-login-card">
                        <div class="ems-kicker">SmartEMS-AI</div>
                        <div class="ems-login-title">系统登录</div>
                        <div class="ems-login-copy">
                            请输入账号和密码，登录后进入电价预测、调度回测和报表分析工作台。
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("账号", placeholder="请输入账号")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            submitted = st.form_submit_button("登录", type="primary", width="stretch")

        if submitted:
            if not is_login_configured():
                st.error("尚未配置登录账号。请先设置 SMARTEMS_USERNAME 和 SMARTEMS_PASSWORD 环境变量。")
            elif verify_login(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("账号或密码错误。")

        st.caption("账号密码从环境变量读取，不写入源码。")


def render_sidebar():
    st.sidebar.title("SmartEMS-AI")
    st.sidebar.caption("智能能源管理电价预测与调度优化平台")
    username = st.session_state.get("username", "未登录")
    st.sidebar.markdown(f'<span class="ems-status">当前用户：{username}</span>', unsafe_allow_html=True)
    if st.sidebar.button("退出登录", width="stretch"):
        st.session_state.pop("authenticated", None)
        st.session_state.pop("username", None)
        st.rerun()
    return st.sidebar.radio(
        "功能导航",
        [
            "系统总览",
            "数据管理",
            "特征工程",
            "模型训练预测",
            "策略回测",
            "报表分析",
        ],
    )


def render_overview():
    render_hero()
    status = get_file_status()

    show_metric_row(
        [
            {"label": "原始 Excel 文件", "value": status["raw_count"]},
            {"label": "处理后数据集", "value": "已生成" if status["merged_exists"] else "未生成"},
            {"label": "特征数据集", "value": "已生成" if status["feature_exists"] else "未生成"},
            {"label": "预测结果文件", "value": status["prediction_count"]},
            {"label": "回测结果", "value": "已生成" if status["backtest_exists"] else "未生成"},
        ]
    )

    render_capability_grid()

    st.subheader("业务流程")
    st.markdown(
        """
        1. 导入日前或实时市场 Excel 数据。
        2. 构建多日机组出力、电价、收益时间序列。
        3. 生成滞后、滚动、差分和时间类预测特征。
        4. 训练 RandomForest、LightGBM 或 XGBoost 电价预测模型。
        5. 基于预测电价执行跟价调度策略和收益回测。
        6. 输出预测结果、策略明细、日度汇总和分析图表。
        """
    )

    merged_path = PROJECT_ROOT / "data" / "processed" / "merged_dataset.csv"
    if merged_path.exists():
        df = load_csv(merged_path, parse_datetime=True)
        st.subheader("基础数据概览")
        show_metric_row(
            [
                {"label": "样本数", "value": f"{len(df):,}"},
                {"label": "平均电价", "value": f"{df['price'].mean():.2f}"},
                {"label": "平均出力", "value": f"{df['power'].mean():.2f} MW"},
                {"label": "总收益", "value": f"{df['revenue'].sum():,.2f}"},
            ]
        )
        st.line_chart(df[["price", "power"]])


def render_data_management():
    render_page_title("数据管理", "预览原始数据文件，按机组名称构建多日基础时间序列。")
    raw_files = list_raw_excel_files()

    left, right = st.columns([1, 2])
    with left:
        st.subheader("原始数据文件")
        st.write("当前目录：`data/raw/origin_dataset`")
        if raw_files:
            selected = st.selectbox("选择 Excel 文件预览", raw_files, format_func=lambda p: p.name)
        else:
            selected = None
            st.warning("未发现原始 Excel 文件。")

        unit_name = st.text_input(
            "机组名称",
            value="华北.昱光/20kV.3#机组",
            help="用于从原始 Excel 中提取指定机组的出力和电价数据。",
        )

        if st.button("构建多日基础数据集", type="primary", width="stretch"):
            with st.spinner("正在读取原始 Excel 并生成 merged_dataset.csv..."):
                df = build_multi_day_dataset(unit_name=unit_name)
            st.success(f"基础数据集已生成，共 {len(df):,} 条记录。")
            st.dataframe(df.head(20), width="stretch")

    with right:
        st.subheader("数据预览")
        if selected:
            try:
                preview = preview_excel_file(selected)
                st.dataframe(preview, width="stretch")
            except Exception as exc:
                st.error(f"Excel 预览失败：{exc}")

        merged_path = PROJECT_ROOT / "data" / "processed" / "merged_dataset.csv"
        if merged_path.exists():
            st.subheader("已生成基础数据集")
            df = load_csv(merged_path, parse_datetime=True)
            st.dataframe(df.tail(20), width="stretch")
            st.download_button(
                "下载 merged_dataset.csv",
                data=merged_path.read_bytes(),
                file_name="merged_dataset.csv",
                mime="text/csv",
            )


def render_feature_engineering():
    render_page_title("特征工程", "构建电价滞后、滚动统计、差分和时间类特征。")
    merged_path = PROJECT_ROOT / "data" / "processed" / "merged_dataset.csv"
    feature_path = PROJECT_ROOT / "data" / "processed" / "feature_dataset.csv"

    if not merged_path.exists():
        st.warning("请先在“数据管理”中构建基础数据集。")
        return

    top_left, top_right = st.columns([1.25, 1])
    with top_left:
        df = load_csv(merged_path, parse_datetime=True)
        show_metric_row(
            [
                {"label": "基础样本数", "value": f"{len(df):,}"},
                {"label": "字段数", "value": len(df.columns)},
                {"label": "起始时间", "value": str(df.index.min())},
                {"label": "结束时间", "value": str(df.index.max())},
            ]
        )
        st.subheader("特征构建配置")
        st.write("系统将生成电价滞后、功率滞后、收益滞后、滚动统计、差分和时间特征。")
        st.code("\n".join(FEATURE_COLUMNS), language="text")

    with top_right:
        if WORKFLOW_IMAGE.exists():
            st.markdown('<div class="ems-image-frame">', unsafe_allow_html=True)
            st.image(str(WORKFLOW_IMAGE), caption="数据到预测再到调度的智能分析流程", width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("生成特征数据集", type="primary"):
        with st.spinner("正在生成 feature_dataset.csv..."):
            feature_df = build_feature_dataset()
        st.success(f"特征数据集已生成，共 {len(feature_df):,} 条记录。")
        st.dataframe(feature_df.head(30), width="stretch")

    if feature_path.exists():
        st.subheader("已生成特征数据集")
        feature_df = load_csv(feature_path, parse_datetime=True)
        st.dataframe(feature_df.tail(30), width="stretch")
        st.download_button(
            "下载 feature_dataset.csv",
            data=feature_path.read_bytes(),
            file_name="feature_dataset.csv",
            mime="text/csv",
        )


def render_model_training():
    render_page_title("模型训练预测", "训练电价预测模型，查看误差指标、预测曲线和模型输出文件。")
    feature_path = PROJECT_ROOT / "data" / "processed" / "feature_dataset.csv"
    if not feature_path.exists():
        st.warning("请先在“特征工程”中生成特征数据集。")
        return

    left, right = st.columns([1, 2])
    with left:
        model_name = st.selectbox("预测模型", ["RandomForest", "LightGBM", "XGBoost"])
        test_size = st.slider("测试集比例", min_value=0.1, max_value=0.4, value=0.2, step=0.05)
        save_model = st.checkbox("保存模型文件", value=True)

        if st.button("开始训练并预测", type="primary", width="stretch"):
            with st.spinner(f"正在训练 {model_name} 模型..."):
                result = train_price_model(
                    model_name=model_name,
                    test_size=test_size,
                    save_model=save_model,
                )
            st.success("模型训练完成。")
            st.session_state["latest_model_result"] = result

    with right:
        result = st.session_state.get("latest_model_result")
        if result:
            show_metric_row(
                [
                    {"label": "MAE", "value": f"{result['mae']:.2f}"},
                    {"label": "RMSE", "value": f"{result['rmse']:.2f}"},
                    {"label": "训练样本", "value": f"{result['train_size']:,}"},
                    {"label": "测试样本", "value": f"{result['test_size']:,}"},
                ]
            )
            st.write(f"预测结果：`{result['result_path']}`")
            if result.get("model_path"):
                st.write(f"模型文件：`{result['model_path']}`")
            st.line_chart(result["result_df"][["real_price", "pred_price"]])
            st.dataframe(result["result_df"].tail(30), width="stretch")
        else:
            st.info("选择模型并点击训练后，这里会显示误差指标、预测曲线和结果表。")


def render_backtest():
    render_page_title("策略回测", "基于预测电价执行跟价调度，输出收益、成本、利润和日度汇总。")
    prediction_files = load_prediction_files()
    if not prediction_files:
        st.warning("请先在“模型训练预测”中生成预测结果。")
        return

    left, right = st.columns([1, 2])
    with left:
        selected = st.selectbox("预测结果文件", prediction_files, format_func=lambda p: p.name)
        initial_power = st.number_input("初始出力 MW", min_value=0.0, max_value=1000.0, value=120.0, step=10.0)
        if st.button("执行策略回测", type="primary", width="stretch"):
            with st.spinner("正在执行跟价策略和调度约束计算..."):
                result = run_strategy_backtest(selected, initial_power=initial_power)
            st.success("策略回测完成。")
            st.session_state["latest_backtest_result"] = result

    with right:
        result = st.session_state.get("latest_backtest_result")
        if result:
            summary = result["summary"]
            show_metric_row(
                [
                    {"label": "总收益", "value": f"{summary['total_revenue']:,.2f}"},
                    {"label": "总成本", "value": f"{summary['total_cost']:,.2f}"},
                    {"label": "总利润", "value": f"{summary['total_profit']:,.2f}"},
                    {"label": "平均出力", "value": f"{summary['avg_power']:.2f} MW"},
                ]
            )
            st.line_chart(result["detail_df"][["real_price", "pred_price", "actual_power"]])
            st.subheader("日度经营汇总")
            st.dataframe(result["daily_df"], width="stretch")
            st.write(f"明细结果：`{result['detail_path']}`")
            st.write(f"日度汇总：`{result['daily_path']}`")
        else:
            st.info("选择预测结果并执行回测后，这里会显示收益、成本、利润和调度曲线。")


def render_reports():
    render_page_title("报表分析", "集中查看预测结果、策略明细、日度汇总和图表文件。")

    report_tabs = st.tabs(["预测结果", "策略回测", "图表文件"])

    with report_tabs[0]:
        files = load_prediction_files()
        if files:
            selected = st.selectbox("选择预测结果", files, format_func=lambda p: p.name, key="report_prediction")
            df = load_csv(selected, parse_datetime=True)
            show_metric_row(
                [
                    {"label": "记录数", "value": f"{len(df):,}"},
                    {"label": "真实均价", "value": f"{df['real_price'].mean():.2f}"},
                    {"label": "预测均价", "value": f"{df['pred_price'].mean():.2f}"},
                ]
            )
            st.line_chart(df[["real_price", "pred_price"]])
            st.dataframe(df, width="stretch")
        else:
            st.info("暂无预测结果文件。")

    with report_tabs[1]:
        detail_path = PROJECT_ROOT / "output" / "strategy_backtest_result.csv"
        daily_path = PROJECT_ROOT / "output" / "daily_strategy_summary.csv"
        if detail_path.exists():
            detail_df = load_csv(detail_path, parse_datetime=True)
            st.line_chart(detail_df[["revenue", "cost", "profit", "actual_power"]])
            st.dataframe(detail_df.tail(50), width="stretch")
        if daily_path.exists():
            st.subheader("日度汇总")
            st.dataframe(load_csv(daily_path), width="stretch")
        if not detail_path.exists() and not daily_path.exists():
            st.info("暂无策略回测结果。")

    with report_tabs[2]:
        image_files = sorted((PROJECT_ROOT / "reports").glob("*.png"))
        image_files += sorted((PROJECT_ROOT / "data" / "output").glob("*.png"))
        if not image_files:
            st.info("暂无图表文件。")
            return
        cols = st.columns(2)
        for index, image_path in enumerate(image_files):
            with cols[index % 2]:
                st.image(str(image_path), caption=image_path.name, width="stretch")


def render_login():
    image_url = image_data_url(HERO_IMAGE)
    _, center, _ = st.columns([1, 1.05, 1])

    with center:
        st.markdown(
            f"""
            <div class="ems-login-bg" style="background-image: url('{image_url}');">
                <div class="ems-login-mask">
                    <div class="ems-login-card">
                        <div class="ems-kicker">SmartEMS-AI</div>
                        <div class="ems-login-title">\u7cfb\u7edf\u767b\u5f55</div>
                        <div class="ems-login-copy">
                            \u8bf7\u8f93\u5165\u8d26\u53f7\u548c\u5bc6\u7801\uff0c\u767b\u5f55\u540e\u8fdb\u5165\u7535\u4ef7\u9884\u6d4b\u3001\u8c03\u5ea6\u56de\u6d4b\u548c\u62a5\u8868\u5206\u6790\u5de5\u4f5c\u53f0\u3002
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("\u8d26\u53f7", placeholder="\u8bf7\u8f93\u5165\u8d26\u53f7")
            password = st.text_input(
                "\u5bc6\u7801",
                type="password",
                placeholder="\u8bf7\u8f93\u5165\u5bc6\u7801",
            )
            submitted = st.form_submit_button("\u767b\u5f55", type="primary", width="stretch")

        if submitted:
            if verify_login(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("\u8d26\u53f7\u6216\u5bc6\u7801\u9519\u8bef\u3002")

        st.caption(
            "\u6f14\u793a\u8d26\u53f7\uff1aadmin\uff0c\u5bc6\u7801\uff1a123456\u3002"
            "\u53ef\u901a\u8fc7 SMARTEMS_USERNAME / SMARTEMS_PASSWORD \u73af\u5883\u53d8\u91cf\u8986\u76d6\u3002"
        )


def render_sidebar():
    st.sidebar.title("SmartEMS-AI")
    st.sidebar.caption("\u667a\u80fd\u80fd\u6e90\u7ba1\u7406\u7535\u4ef7\u9884\u6d4b\u4e0e\u8c03\u5ea6\u4f18\u5316\u5e73\u53f0")
    username = st.session_state.get("username", "\u672a\u767b\u5f55")
    st.sidebar.markdown(
        f'<span class="ems-status">\u5f53\u524d\u7528\u6237\uff1a{username}</span>',
        unsafe_allow_html=True,
    )
    if st.sidebar.button("\u9000\u51fa\u767b\u5f55", width="stretch"):
        st.session_state.pop("authenticated", None)
        st.session_state.pop("username", None)
        st.rerun()

    return st.sidebar.radio(
        "\u529f\u80fd\u5bfc\u822a",
        [
            "\u7cfb\u7edf\u603b\u89c8",
            "\u6570\u636e\u7ba1\u7406",
            "\u7279\u5f81\u5de5\u7a0b",
            "\u6a21\u578b\u8bad\u7ec3\u9884\u6d4b",
            "\u7b56\u7565\u56de\u6d4b",
            "\u62a5\u8868\u5206\u6790",
        ],
    )


def initialize_auth_state():
    if (
        st.session_state.get("auth_flow_version") != AUTH_FLOW_VERSION
        or st.session_state.get("app_boot_id") != APP_BOOT_ID
    ):
        st.session_state["auth_flow_version"] = AUTH_FLOW_VERSION
        st.session_state["app_boot_id"] = APP_BOOT_ID
        st.session_state["authenticated"] = False
        st.session_state.pop("username", None)


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="EMS",
        layout="wide",
    )
    apply_theme()
    initialize_auth_state()
    if not st.session_state.get("authenticated"):
        render_login()
        return

    page = render_sidebar()

    if page == "系统总览":
        render_overview()
    elif page == "数据管理":
        render_data_management()
    elif page == "特征工程":
        render_feature_engineering()
    elif page == "模型训练预测":
        render_model_training()
    elif page == "策略回测":
        render_backtest()
    else:
        render_reports()
