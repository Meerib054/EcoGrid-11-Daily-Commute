import streamlit as st


if "best_carbon" not in st.session_state:
    st.session_state.best_carbon = float("inf")

if "stage" not in st.session_state:
    st.session_state.stage = 0
    st.session_state.carbon = 0
    st.session_state.time = 0
    st.session_state.streak = 0
    st.session_state.mall_visited = False

scenarios = [
    {
        "story": "7:00 AM — MORNING HEAT: It's already sweltering outside. You need to cool your room while getting ready, but you're short on time.",
        "image": "getting-ready.gif",
        "choices": [
            {"text": "Blast the central AC at 18°C with doors wide open to cool down instantly", "carbon": 14, "time": 1, "is_eco": False},
            {"text": "Turn on a low-energy ceiling fan and open high windows for air flow", "carbon": 1, "time": 8, "is_eco": True},
            {"text": "Leave the window AC unit running on eco-mode while you take a long shower", "carbon": 8, "time": 3, "is_eco": False}
        ]
    },
    {
        "story": "7:30 AM — WATER HYGIENE: You need to brush your teeth and wash up before heading out.",
        "image": "brushing.gif",
        "choices": [
            {"text": "Let hot water run continuously so it stays warm for rinsing", "carbon": 6, "time": 2, "is_eco": False},
            {"text": "Use cold water in a small mug and turn off the tap completely between rinses", "carbon": 0, "time": 7, "is_eco": True}
        ]
    },
    {
        "story": "8:00 AM — THE MORNING COMMUTE: Heavy rain hits suddenly. You are running 10 minutes late for your presentation!",
        "image": "rain.gif",
        "choices": [
            {"text": "Order an express private gas taxi to drop you directly at the door", "carbon": 18, "time": 12, "is_eco": False},
            {"text": "Slightly risk being late: Walk 10 mins in rain gear to catch the high-speed electric metro", "carbon": 2, "time": 30, "is_eco": True},
            {"text": "Take a shared diesel commuter van that skips metro lines", "carbon": 10, "time": 20, "is_eco": False}
        ]
    },
    {
        "story": "8:30 AM — GRIDLOCK EMBARGO: Highway 4 is completely locked. Drivers are idling everywhere.",
        "image": "highway-lock.gif",
        "choices": [
            {"text": "Pay extra toll for a single-occupant express bypass highway line", "carbon": 15, "time": 10, "is_eco": False},
            {"text": "Abandon vehicle travel: Switch to a city rental kick-scooter in the rain", "carbon": 1, "time": 22, "is_eco": True},
            {"text": "Wait it out idling in your vehicle while blasting the radio", "carbon": 12, "time": 35, "is_eco": False}
        ]
    },
    {
        "story": "10:30 AM — MORNING COFFEE: You need a quick caffeine boost before your meeting.",
        "image": "coffee.gif",
        "choices": [
            {"text": "Grab a single-use plastic cup with a plastic straw from the drive-thru window", "carbon": 7, "time": 3, "is_eco": False},
            {"text": "Wait in a long 15-minute queue to get poured into your personal thermal mug", "carbon": 1, "time": 15, "is_eco": True}
        ]
    },
    {
        "story": "12:30 PM — LUNCHTIME RUSH: You have 30 minutes before your next shift. Options are limited.",
        "image": "lunch.gif",
        "choices": [
            {"text": "Order high-speed motorbike delivery (heavy plastic wrap & imported red meat burger)", "carbon": 16, "time": 8, "is_eco": False},
            {"text": "Walk 12 minutes to a local organic farm-to-table cooperative with ceramic plates", "carbon": 1, "time": 28, "is_eco": True},
            {"text": "Grab a pre-packaged convenience store meal containing single-use utensils", "carbon": 8, "time": 10, "is_eco": False}
        ]
    },
    {
        "story": "1:30 PM — WASTE MANAGEMENT: You finished your meal. The public sorting bins nearby are broken and locked.",
        "image": "trash.gif",
        "choices": [
            {"text": "Dump all mixed waste into a single overflowing street trash bin", "carbon": 11, "time": 1, "is_eco": False},
            {"text": "Pack all greasy packaging and cans in your bag to sort at home later", "carbon": 0, "time": 6, "is_eco": True}
        ]
    },
    {
        "story": "3:00 PM — PRINTING DEMANDS: You need to hand out notes to 5 colleagues for a brainstorm session.",
        "image": "nb.gif",
        "choices": [
            {"text": "Print full-color single-sided thick glossy pages on fresh paper", "carbon": 9, "time": 2, "is_eco": False},
            {"text": "Spend 10 minutes setting up a shared cloud link and projection display instead", "carbon": 0, "time": 10, "is_eco": True}
        ]
    },
    {
        "story": "4:30 PM — CLIMATE CONTROL DISPUTE: The study lounge is freezing, but someone left the window open with the AC blasting.",
        "image": "ac.gif",
        "choices": [
            {"text": "Ignore it—facility management will shut down building power tonight anyway", "carbon": 13, "time": 1, "is_eco": False},
            {"text": "Take 5 minutes to adjust thermostat presets, shut window seals, and notify staff", "carbon": 0, "time": 6, "is_eco": True}
        ]
    },
    {
        "story": "5:30 PM — SHOPPING & SUPPLIES: You need to pick up a few household groceries before going home.",
        "image": "grocery.gif",
        "choices": [
            {"text": "Buy air-freighted imported berries wrapped in double plastic containers", "carbon": 12, "time": 5, "is_eco": False},
            {"text": "Walk 15 minutes out of your way to buy locally grown open-basket seasonal produce", "carbon": 1, "time": 20, "is_eco": True}
        ]
    },
    {
        "story": "6:30 PM — FREE TIME CHOICE: You meet your friends. Everyone is deciding where to hang out.",
        "image": "hang-out.gif",
        "choices": [
            {"text": "Go to the commercial mega-mall with high air-conditioning emissions", "carbon": 14, "time": 15, "is_eco": False},
            {"text": "Head to the community eco-park with free public green spaces", "carbon": 0, "time": 25, "is_eco": True},
            {"text": "Go home and run multiple high-power gaming rigs on separate rooms", "carbon": 8, "time": 10, "is_eco": False}
        ]
    },
    {
        "story": "8:00 PM — EVENING LAUNDRY: Your outfit for tomorrow's competition needs to be cleaned.",
        "image": "laundry.gif",
        "choices": [
            {"text": "Run a small half-load on express thermal hot water and tumble dry on high heat", "carbon": 16, "time": 30, "is_eco": False},
            {"text": "Combine with family laundry, run cold eco-wash, and hang dry overnight", "carbon": 1, "time": 65, "is_eco": True}
        ]
    },
    {
        "story": "9:30 PM — RESIDENTIAL ENERGY: Your family is watching TV in the living room while room lights are on in empty rooms.",
        "image": "lights.gif",
        "choices": [
            {"text": "Leave all lights and standby devices plugged in around the home", "carbon": 10, "time": 1, "is_eco": False},
            {"text": "Walk through the house turning off unused lighting and switching off power strips", "carbon": 0, "time": 8, "is_eco": True}
        ]
    },
    {
        "story": "10:30 PM — NIGHTTIME TECH CHARGING: Your tablet, phone, and power bank all need charging overnight.",
        "image": "charging.gif",
        "choices": [
            {"text": "Plug all 3 devices into fast-charging bricks left in sockets all night long", "carbon": 7, "time": 1, "is_eco": False},
            {"text": "Plug them into an eco-smart smart strip with automated 2-hour safety shut-off timers", "carbon": 0, "time": 5, "is_eco": True}
        ]
    },
    {
        "story": "11:00 PM — SLEEP CLIMATE: Settling into bed. How are you setting up your room temperature for the 8-hour sleep?",
        "image": "sleep.gif",
        "choices": [
            {"text": "Set AC to freezing 16°C and sleep under heavy thick blankets", "carbon": 18, "time": 1, "is_eco": False},
            {"text": "Set AC to optimal 24°C combined with sleep-timer mode and ceiling fan", "carbon": 2, "time": 3, "is_eco": True}
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
dash_col1, dash_col2 = st.columns(2)


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
st.write("---")

if st.session_state.stage<len(scenarios):
    current=scenarios[st.session_state.stage]

    st.subheader(f"Stage {st.session_state.stage + 1} of {len(scenarios)}")

    if "image" in current:
        st.image(current["image"], use_container_width=True)

    st.write(current["story"])
    
    if st.session_state.streak >0:
        st.info(f"🔥 Green Streak: {st.session_state.streak}")

    st.write("")

    for choice in current["choices"]:
        if st.button(choice["text"]):
            if "mega-mall" in choice["text"]:
                st.session_state.mall_visited=True

            st.session_state.carbon += choice["carbon"]
            st.session_state.time += choice["time"]

            #the positive sound thing
            if choice["is_eco"]:
                st.audio("https://www.soundjay.com/buttons/sounds/button-09a.mp3", autoplay=True)
                st.session_state.streak+=1
                if st.session_state.streak >=3:
                    st.toast("⚡ Multiplier Active: Eco Champion! Bonus -3 Carbon!", icon="🌿")
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
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Carbon Footprint (kg CO₂)", value=st.session_state.carbon)
    with col2:
        st.metric(label="Total Travel Time (minutes)", value=st.session_state.time)
    
    st.write("---")

    if st.session_state.carbon < st.session_state.best_carbon:
        st.session_state.best_carbon = st.session_state.carbon
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
        st.session_state.mall_visited = False
        st.rerun()
