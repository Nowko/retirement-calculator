import streamlit as st

def retirement_income(start_age, monthly_saving, saving_years, defer_years, retirement_years, annual_return_rate, annual_inflation_rate):
    months_saving = saving_years * 12
    r_monthly = (1 + annual_return_rate) ** (1/12) - 1
    balance = 0
    for _ in range(months_saving):
        balance = balance * (1 + r_monthly) + monthly_saving
    months_defer = defer_years * 12
    for _ in range(months_defer):
        balance = balance * (1 + r_monthly)
    months_retirement = retirement_years * 12
    r_real = ((1 + annual_return_rate) / (1 + annual_inflation_rate)) - 1
    r_real_monthly = (1 + r_real) ** (1/12) - 1
    if r_real_monthly == 0:
        monthly_income = balance / months_retirement
    else:
        monthly_income = balance * r_real_monthly / (1 - (1 + r_real_monthly) ** (-months_retirement))
    return monthly_income, balance

st.title("은퇴 저축 결과 계산기")

st.sidebar.header("입력값 설정")
start_age = st.sidebar.number_input("현재 나이", value=30, min_value=0, max_value=100)
monthly_saving_10k = st.sidebar.number_input("매달 저축액 (만원)", value=10, step=1)
monthly_saving = monthly_saving_10k * 10000
saving_years = st.sidebar.number_input("저축 기간 (년)", value=20, min_value=1, max_value=100)
retirement_start_age = st.sidebar.number_input("수령 시작 나이", value=60, min_value=0, max_value=100)
default_retirement_end_age = 90
retirement_years = st.sidebar.number_input("은퇴 후 수령 기간 (년) (기본 90세까지)", value=default_retirement_end_age - retirement_start_age, min_value=1, max_value=60)
st.sidebar.caption(f"{retirement_start_age + retirement_years}세까지 연금을 받습니다.")
annual_return_rate = st.sidebar.number_input("연 수익률 (%)", value=2.7, step=0.1) / 100
annual_inflation_rate = st.sidebar.number_input("연 물가상승률 (%)", value=2.1, step=0.1) / 100

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='text-align: center; font-size: 12px;'>Made by <b>NOWKO</b> on Brunch</div>", unsafe_allow_html=True)

saving_end_age = start_age + saving_years
defer_years = retirement_start_age - saving_end_age

if defer_years < 0:
    st.error("수령 시작 나이는 저축 종료 나이 이후여야 합니다. 다시 입력해 주세요.")
else:
    if st.button("🧮 계산하기"):
        monthly_income_today_value, total_balance = retirement_income(
            start_age, monthly_saving, saving_years, defer_years, retirement_years, annual_return_rate, annual_inflation_rate
        )
        months_retirement = retirement_years * 12
        r_monthly = (1 + annual_return_rate) ** (1/12) - 1
        if r_monthly == 0:
            monthly_income_nominal = total_balance / months_retirement
        else:
            monthly_income_nominal = total_balance * r_monthly / (1 - (1 + r_monthly) ** (-months_retirement))

        st.subheader("📌 계산 결과")
        st.markdown(f"""
        지금 매달 **{monthly_saving_10k:,}만원**씩 저축하면,

        📤 은퇴 후 매달 수령 금액: **{monthly_income_nominal / 10000:,.1f}만원**  
        🪙 실제 구매력 기준(오늘 가치): **{monthly_income_today_value / 10000:,.1f}만원**
        """)
        st.caption("※ 기본 설정은 연금을 90세에 종료하는 것으로 가정되어 있으며, 수령 기간을 조정할 수 있습니다.")
        st.caption("※ 매년 물가상승률만큼 인상된 금액으로 수령하여, 실질 구매력은 고정되도록 설계되었습니다.")
        st.markdown("---")
        st.markdown("""
<div style='background-color: #e8f0fe; padding: 15px; border-radius: 6px; font-size: 15px; color: #1a1a1a;'>
💡 <strong>복리는 돈을 키워주는 마법처럼 들리지만,</strong><br>
사실은 계속 오르는 물가를 간신히 따라가는 기본 체력일 뿐입니다.<br><br>
복리와 시간이 아무리 오래 작동해도,<br>
결국 살 수 있는 물건은 그대로예요.<br>
숫자만 커질 뿐, <strong>내 삶의 질이 더 나아지진 않습니다.</strong><br><br>
그래서 '빨리 시작하라'는 말은,<br>
부자가 되라는 말이 아니라<br>
<strong>더 가난해지지 않기 위한 현실 방어 전략</strong>입니다.
</div>
""", unsafe_allow_html=True)
