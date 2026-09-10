import streamlit as st


st.cache_data.clear()
st.cache_resource.clear()


st.set_page_config(page_title="EcoGrid: SDG 11 Challenge", layout="centered")
st.markdown("""
<style>
    .stApp { background-color: #2b090a; }
    [data-testid="stSidebar"] {background-color: #4a1014; border-right: 2px solid #6b1418; }
</style>
""", unsafe_allow_html=True)

if "best_carbon" not in st.session_state:
    try:
        with open("highscore.txt", "r") as f:
            st.session_state.best_carbon = float(f.read())
    except:
        st.session_state.best_carbon = float("inf")

if "stage" not in st.session_state:
    st.session_state.stage = 0
    st.session_state.carbon = 0
    st.session_state.time = 0
    st.session_state.streak = 0
    st.session_state.money = 100
    st.session_state.mall_visited = False

scenarios = [
    {
        "story": "7:00 AM — MORNING HEAT: It's sweltering outside. You need to cool your room while getting ready.",
        "image": "getting-ready.gif",
        "choices": [
            {"text": "Blast central AC at 18°C with doors wide open", "carbon": 14, "time": 1, "cost": 15, "is_eco": False},
            {"text": "Turn on a low-energy ceiling fan and open high windows", "carbon": 1, "time": 8, "cost": 2, "is_eco": True},
            {"text": "Leave window AC unit running on eco-mode while taking a shower", "carbon": 8, "time": 3, "cost": 8, "is_eco": False}
        ]
    },
    {
        "story": "7:30 AM — WATER HYGIENE: You need to brush your teeth and wash up before heading out.",
        "image": "brushing.gif",
        "choices": [
            {"text": "Let hot water run continuously for easy rinsing", "carbon": 6, "time": 2, "cost": 10, "is_eco": False},
            {"text": "Use cold water in a mug and turn off the tap completely", "carbon": 0, "time": 7, "cost": 0, "is_eco": True}
        ]
    },
    {
        "story": "8:00 AM — THE MORNING COMMUTE: Heavy rain hits! You are running 10 minutes late.",
        "image": "rain.gif",
        "choices": [
            {"text": "Order an express private gas taxi to drop you at the door", "carbon": 18, "time": 12, "cost": 30, "is_eco": False},
            {"text": "Walk 10 mins in rain gear to catch the high-speed electric metro", "carbon": 2, "time": 30, "cost": 5, "is_eco": True},
            {"text": "Take a shared diesel commuter van", "carbon": 10, "time": 20, "cost": 12, "is_eco": False}
        ]
    },
    {
        "story": "8:30 AM — GRIDLOCK EMBARGO: Highway 4 is locked. Drivers are idling everywhere.",
        "image": "highway-lock.gif",
        "choices": [
            {"text": "Pay extra toll for a single-occupant express bypass highway line", "carbon": 15, "time": 10, "cost": 25, "is_eco": False},
            {"text": "Switch to a city rental kick-scooter in the bike lane", "carbon": 1, "time": 22, "cost": 4, "is_eco": True},
            {"text": "Wait it out idling in your vehicle while blasting the radio", "carbon": 12, "time": 35, "cost": 8, "is_eco": False}
        ]
    },
    {
        "story": "10:30 AM — MORNING COFFEE: You need a quick caffeine boost before your meeting.",
        "image": "coffee.gif",
        "choices": [
            {"text": "Grab a single-use plastic cup from the drive-thru window", "carbon": 7, "time": 3, "cost": 8, "is_eco": False},
            {"text": "Wait in a queue to fill your personal mug (get a \$2 discount)", "carbon": 1, "time": 15, "cost": 4, "is_eco": True}
        ]
    },
    {
        "story": "12:30 PM — LUNCHTIME RUSH: You have 30 minutes before your next shift.",
        "image": "lunch.gif",
        "choices": [
            {"text": "Order high-speed motorbike delivery (heavy plastic wrap & imported meat)", "carbon": 16, "time": 8, "cost": 22, "is_eco": False},
            {"text": "Walk 12 minutes to a local organic farm-to-table coop", "carbon": 1, "time": 28, "cost": 10, "is_eco": True},
            {"text": "Grab a pre-packaged convenience store meal", "carbon": 8, "time": 10, "cost": 14, "is_eco": False}
        ]
    },
    {
        "story": "1:30 PM — WASTE MANAGEMENT: You finished lunch. Public sorting bins are broken.",
        "image": "trash.gif",
        "choices": [
            {"text": "Dump all mixed waste into an overflowing street trash bin", "carbon": 11, "time": 1, "cost": 0, "is_eco": False},
            {"text": "Pack all packaging in your bag to sort at home (earn \$5 recycling reward later)", "carbon": 0, "time": 6, "cost": -5, "is_eco": True}
        ]
    },
    {
        "story": "3:00 PM — PRINTING DEMANDS: You need to hand out notes to 5 colleagues for a brainstorm.",
        "image": "nb.gif",
        "choices": [
            {"text": "Print full-color single-sided thick glossy pages", "carbon": 9, "time": 2, "cost": 12, "is_eco": False},
            {"text": "Spend 10 minutes setting up a shared cloud link and projector", "carbon": 0, "time": 10, "cost": 0, "is_eco": True}
        ]
    },
    {
        "story": "4:30 PM — CLIMATE CONTROL DISPUTE: Study lounge is freezing, window left open with AC blasting.",
        "image": "ac.gif",
        "choices": [
            {"text": "Ignore it—facility management will shut down power tonight anyway", "carbon": 13, "time": 1, "cost": 0, "is_eco": False},
            {"text": "Take 5 minutes to adjust thermostat presets and notify staff (Eco-rebate)", "carbon": 0, "time": 6, "cost": -10, "is_eco": True}
        ]
    },
    {
        "story": "5:30 PM — SHOPPING & SUPPLIES: Pick up household groceries before heading home.",
        "image": "grocery.gif",
        "choices": [
            {"text": "Buy air-freighted imported berries in double plastic containers", "carbon": 12, "time": 5, "cost": 18, "is_eco": False},
            {"text": "Walk 15 minutes out of your way for locally grown seasonal produce", "carbon": 1, "time": 20, "cost": 7, "is_eco": True}
        ]
    },
    {
        "story": "6:30 PM — FREE TIME CHOICE: Meeting friends. Everyone is deciding where to hang out.",
        "image": "hang-out.gif",
        "choices": [
            {"text": "Go to the commercial mega-mall with high air-conditioning emissions", "carbon": 14, "time": 15, "cost": 25, "is_eco": False},
            {"text": "Head to the community eco-park with free public green spaces", "carbon": 0, "time": 25, "cost": 0, "is_eco": True},
            {"text": "Go home and run multiple high-power gaming rigs in separate rooms", "carbon": 8, "time": 10, "cost": 10, "is_eco": False}
        ]
    },
    {
        "story": "8:00 PM — EVENING LAUNDRY: Your outfit for tomorrow needs to be cleaned.",
        "image": "laundry.gif",
        "choices": [
            {"text": "Run a half-load on express hot water and tumble dry on high heat", "carbon": 16, "time": 30, "cost": 15, "is_eco": False},
            {"text": "Combine with family laundry, run cold eco-wash, and hang dry overnight", "carbon": 1, "time": 65, "cost": 2, "is_eco": True}
        ]
    },
    {
        "story": "9:30 PM — RESIDENTIAL ENERGY: TV is on while lights run in empty rooms.",
        "image": "lights.gif",
        "choices": [
            {"text": "Leave all lights and standby devices plugged in around the home", "carbon": 10, "time": 1, "cost": 12, "is_eco": False},
            {"text": "Walk through the house turning off unused lighting and power strips", "carbon": 0, "time": 8, "cost": 0, "is_eco": True}
        ]
    },
    {
        "story": "10:30 PM — NIGHTTIME TECH CHARGING: Tablet, phone, and power bank all need charging.",
        "image": "charging.gif",
        "choices": [
            {"text": "Plug all 3 devices into fast-charging bricks left in sockets all night", "carbon": 7, "time": 1, "cost": 6, "is_eco": False},
            {"text": "Plug into an eco-smart strip with automated shut-off timers", "carbon": 0, "time": 5, "is_eco": True, "cost": 1}
        ]
    },
    {
        "story": "11:00 PM — SLEEP CLIMATE: Setting up room temperature for 8 hours of sleep.",
        "image": "sleep.gif",
        "choices": [
            {"text": "Set AC to freezing 16°C and sleep under heavy thick blankets", "carbon": 18, "time": 1, "cost": 20, "is_eco": False},
            {"text": "Set AC to optimal 24°C combined with sleep-timer mode and ceiling fan", "carbon": 2, "time": 3, "cost": 4, "is_eco": True}
        ]
    }
]    

with st.sidebar:
    st.header("🌍 About SDG 11")
    st.write(
        "Sustainable Cities and Communities aims to make urban centers inclusive, safe, resilient, and sustainable."
    )
    st.markdown("---")
    st.subheader("📊 The Problem")
    st.write(
        "Urban transport, energy waste, and poor recycling habits heavily drive up city emissions. Hard trade-offs are necessary!"
    )
    st.markdown("---")
    
    # for high score
    if st.session_state.best_carbon != float("inf"):
        st.metric(label="🏆 Lowest Carbon Run", value=f"{st.session_state.best_carbon} kg CO₂")
    else:
        st.caption("Complete a run to set your high score!")
        
    st.markdown("---")
    st.caption("Developed for Digifest 2026")

    st.title("Green Commuter Challenge 🚶‍♂️🚌")

st.write("### 🏙️ City Status Live Dashboard")
dash_col1, dash_col2, dash_col3= st.columns(3)


with dash_col1:
    if st.session_state.carbon <= 25:
        st.success("🍃 Air Quality: CLEAN")
    elif st.session_state.carbon <= 75:
        st.warning("😷 Air Quality: MODERATE")
    else:
        st.error("🚨 Air Quality: HAZARDOUS")

with dash_col2:
    if st.session_state.time <= 120:
        st.success("🟢 Gridlock Level: LOW")
    elif st.session_state.time <= 220:
        st.warning("🟡 Gridlock Level: MODERATE")
    else:
        st.error("🔴 Gridlock Level: HIGH TRAFFIC")

with dash_col3:
    if st.session_state.money > 30:
        st.success(f"💵 Budget: \${st.session_state.money}")
    elif st.session_state.money > 0:
        st.warning(f"⚠️ Budget: \${st.session_state.money}")
    else:
        st.error(f"💸 Budget: \${st.session_state.money}")

st.write("---")

if st.session_state.money <=0:
    st.error("💸 BANKRUPT! You ran out of money and could not complete your day's journey.")
    st.write("Living sustainably often saves money in the long run. High-convenience options quickly drained your funds!")

    if st.button("Try Again"):
        st.session_state.stage = 0
        st.session_state.carbon = 0
        st.session_state.time = 0
        st.session_state.money = 100
        st.session_state.streak = 0
        st.session_state.mall_visited = False
        st.rerun()

elif st.session_state.stage<len(scenarios):
    current=scenarios[st.session_state.stage]

    st.subheader(f"Stage {st.session_state.stage + 1} of {len(scenarios)}")

    if "image" in current:
        st.image(current["image"], use_container_width=True)

    st.write(current["story"])
    
    if st.session_state.streak >0:
        st.info(f"🔥 Green Streak: {st.session_state.streak}")

    st.write("")

    for choice in current["choices"]:
        cost_text = f" Earns +AED{abs(choice['cost'])}" if choice['cost'] < 0 else (f" Costs AED{choice['cost']}" if choice['cost'] > 0 else " Free")
        button_label = f"{choice['text']} [{cost_text}]"

        if st.button(button_label):
            if "mega-mall" in choice["text"]:
                st.session_state.mall_visited=True

            st.session_state.carbon += choice["carbon"]
            st.session_state.time += choice["time"]
            st.session_state.money -= choice["cost"]

            #the positive sound thing
            if choice["is_eco"]:
                st.audio("https://www.soundjay.com/buttons/sounds/button-09a.mp3", autoplay=True)
                st.session_state.streak+=1
                if st.session_state.streak >=5:
                    st.toast("⚡ Multiplier Active: Eco Champion! Bonus -2 Carbon!", icon="🌿")
                    st.session_state.carbon = max(0, st.session_state.carbon - 2)

            else:
                st.audio("https://www.soundjay.com/transportation/sounds/car-horn-7.mp3", autoplay=True)
                if st.session_state.streak >= 1:
                    st.toast("Streak broken! Carbon emissions increased.", icon="💨")
                st.session_state.streak = 0
            
            st.session_state.stage+=1
            st.rerun()

else:
    st.success("You've completed the challenge!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Carbon Footprint (kg CO₂)", value=st.session_state.carbon)
    with col2:
        st.metric(label="Total Travel Time (minutes)", value=st.session_state.time)
    with col3:
        st.metric(label="Remaining Money", value=f"${st.session_state.money}")
    
    st.write("---")

    if st.session_state.carbon < st.session_state.best_carbon:
        st.session_state.best_carbon = st.session_state.carbon
        with open("highscore.txt", "w") as f:
            f.write(str(st.session_state.best_carbon))
        st.toast("🎉 New Personal Best Score Saved!", icon="🏆")
    

    st.write("### 🏅 Achievements Unlocked")
    
    with st.expander("Click to view your unlocked archive badges"):

        if st.session_state.carbon <= 25:
            st.write("🟢 **[UNLOCKED] Zero Carbon Hero:** Finished with an ultra-low emission score!")
        else:
            st.write("❌ *[LOCKED] Zero Carbon Hero* (Finish with <= 25kg CO₂)")
            
        if st.session_state.time < 5:
            st.write("⚡ **[UNLOCKED] Speed Demon:** Finished your day's journey in under 5 minutes!")
        else:
            st.write("❌ *[LOCKED] Speed Demon* (Finish with total travel time under 5 minutes)")
            
        if st.session_state.mall_visited:
            st.write("🛍️ **[UNLOCKED] Mall Rat:** Visited the commercial mega-mall over natural green spaces.")
        else:
            st.write("❌ *[LOCKED] Mall Rat* (Choose the mega-mall option during your free time stage)")
    
    st.write("---")
    
    if st.session_state.carbon <= 25:
        st.balloons()
        st.subheader("🏆 SDG 11 Champion!")
        st.write("Your entire daily routine was remarkably clean trotz bad weather and tight deadlines!")
        st.balloons()
    elif st.session_state.carbon <= 75:
        st.subheader("👍 Active Citizen!")
        st.write("You made solid eco-friendly choices under pressure, but convenient emissions caught up with you.")
    else:
        st.subheader("🚗 Heavy Carbon Footprint!")
        st.write("High-convenience choices triggered heavy emissions and air quality warnings. Can you beat it next run?")
        
    st.write("")
    if st.button("Restart Game"):
        st.session_state.stage = 0
        st.session_state.carbon = 0
        st.session_state.time = 0
        st.session_state.streak = 0
        st.session_state.money = 100
        st.session_state.mall_visited = False
        st.rerun()
