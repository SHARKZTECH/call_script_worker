import logging
import ollama
from tools.logger import setup_logger


logger = setup_logger(__name__)

# MODEL_NAME = "llama3.2:1b"
MODEL_NAME = "llama3.1:8b"


def generate_call_script(user_name, call_reason, user_company, job_title, industry="General", tone="Formal", language="english"):
    """Generate a structured, dynamic, and conversational sales call script following all best practices."""

    try:
        call_reason = call_reason or "No reason specified"
        user_company = user_company or "Unknown Company"
        job_title = job_title or "Unknown Role"
        industry = industry or "General"

        tone_descriptions = {
            "Formal": "Use a professional, business-oriented tone, which is best for corporate and high-stakes scenarios.",
            "Casual": "Use a friendly, informal tone, which is best for engaging leads and building rapport quickly.",
            "Persuasive": "Use an engaging, persuasive tone that encourages action, ideal for decision-makers or tough objections.",
        }
        tone_instruction = tone_descriptions.get(
            tone, "Use a formal, professional tone.")

        industry_benefits = {
            "Technology": f"optimize workflows and improve operational efficiency using AI-driven solutions that adapt to {user_company}'s needs.",
            "Finance": f"enhance financial planning through data-driven insights and automation, streamlining {user_company}'s financial management.",
            "Healthcare": f"optimize patient care while ensuring compliance and security, specifically suited to {user_company}'s healthcare infrastructure.",
            "Retail": f"improve customer experience with smart analytics and optimized inventory management, tailored to {user_company}'s market.",
            "Manufacturing": f"increase productivity through automation and smarter supply chain management, directly addressing {user_company}'s production goals.",
            "General": f"help businesses like {user_company} streamline their operations and drive growth by improving efficiency and reducing costs."
        }
        value_proposition = industry_benefits.get(
            industry, industry_benefits["General"])

        prompt = f"""
        You are a professional sales agent making a cold call to a potential customer. 
        Follow this **exact structure** to generate an engaging and effective call script:
        Answer the following call script generation request in {language}

        ---
        **Admin Approach - Connecting with the Decision Maker (DM)**  
        (Use a casual, natural approach to get past the gatekeeper.)  
        - "Hi there, could you connect me to {user_name}, please?"
        - "Good morning! Can you help me find {user_name}, please?"
        - "Hi, I was hoping to speak with {user_name}. Is {user_name} available?"
        
        ---
        **Opening & Greeting (When Speaking to the DM)**  
        - Confirm you’re speaking with {user_name}.  
        - Start with a warm, professional greeting.  
        - Example: "Hello, is this {user_name}? Hope you’re having a great day."

        ---
        **Introduction & Value Proposition**  
        - Introduce yourself **briefly** and focus on how you **help businesses** rather than selling upfront.  
        - Example:  
          "I’m reaching out from {user_company}. We work with companies in {industry} to {value_proposition}.  
          Just wanted to see if this is something that might be useful for you."

        ---
        **Need Discovery (C.L.P.R. Framework)**  
        (Encourage the prospect to share insights rather than just answering "yes" or "no.")  
        - **C - Current Situation:** "How do you currently handle [problem area]?"  
        - **L - Likes:** "What’s been working well for you so far?"  
        - **P - Problems:** "Are there any challenges you’ve been facing with your current approach?"  
        - **R - Remedy:** "A lot of companies in your space have been able to fix that by [solution]. Would you be interested in exploring that?"

        ---
        **Handling Common Objections**  
        (Provide **engaging**, **conversational** responses for each common objection.)  
        - **Price Concern:**  
          "Totally understand that budgets are tight. Many of our clients found that our solution actually pays for itself through [ROI/efficiency gains].  
          If cost is a concern, we could look at a phased rollout or a smaller-scale implementation."  
        - **Already Have a Vendor:**  
          "That’s great! We often complement existing solutions rather than replacing them. Would you be open to seeing how we can add value?"  
        - **Not Interested:**  
          "I hear you! A lot of our customers felt the same way at first, but after learning more, they saw real benefits. Would it be worth a quick chat?"  
        - **Timing Issue:**  
          "No worries! When do you think would be a better time to revisit this?"  
        - **Not the Right Person:**  
          "Got it! Who would be the best person for this conversation on your team?"  

        ---
        **Closing & Call-to-Action (CTA)**  
        (Offer multiple options for next steps.)  
        - "Would you be open to a quick 15-minute call next week?"  
        - "I’d love to set up a quick demo so you can see exactly how this works."  
        - "If you'd prefer, I can send over some case studies and follow up in a few days."  
        - "Would it make sense to do a small-scale test so you can evaluate the results firsthand?"

        ---
        **Additional Notes:**  
        - Keep it **conversational and natural** rather than sounding like a script.  
        - Adapt your tone and approach based on their responses.  
        - **Tone:** {tone_instruction}

        Generate this call script **exactly** in the structured format above, making it **dynamic, engaging, and customer-focused**.

        The script should be in user's langauge {language}
        """

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.5}
        )

        if "message" in response and "content" in response["message"]:
            return response["message"]["content"].strip()
        else:
            raise ValueError("Unexpected response format from Ollama.")

    except Exception as e:
        logger.error(f"❌ Error generating call script: {e}", exc_info=True)
        return None


def main():
    """Main function to execute the call script pipeline."""
    logger.info("🚀 Running call script generation pipeline...")

    call_script_formal = generate_call_script(
        "Jack Davis", "Discuss partnership", "TechCorp", "CTO", tone="Formal", language="english")
    call_script_casual = generate_call_script(
        "Jack Davis", "Discuss partnership", "TechCorp", "CTO", tone="Casual", language="spanish")
    call_script_persuasive = generate_call_script(
        "Jack Davis", "Discuss partnership", "TechCorp", "CTO", tone="Persuasive", language="german")

    if call_script_formal:
        print("\n📞 **Formal Call Script:**\n")
        print(call_script_formal)

    if call_script_casual:
        print("\n😃 **Casual Call Script:**\n")
        print(call_script_casual)

    if call_script_persuasive:
        print("\n🔥 **Persuasive Call Script:**\n")
        print(call_script_persuasive)


if __name__ == "__main__":
    main()
