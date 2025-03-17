import logging
import ollama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_call_script(user_name, call_reason, user_company, job_title, tone="Formal"):
    """Generate a call script using user details and specified tone."""
    try:
        call_reason = call_reason or "No reason specified"
        user_company = user_company or "Unknown Company"
        job_title = job_title or "Unknown Role"

        tone_descriptions = {
            "Formal": "Use a professional, business-oriented tone with structured and polite language.",
            "Casual": "Use a friendly and informal tone, making the conversation feel natural and relaxed.",
            "Persuasive": "Use a persuasive and engaging tone, emphasizing benefits and encouraging action."
        }

        tone_instruction = tone_descriptions.get(
            tone, tone_descriptions["Formal"])

        prompt = f"""
		You are a professional call agent. Generate a structured call script for {user_name}, a representative from {user_company}. The tone should be {tone_instruction}.

		- User Name: {user_name}
		- Company: {user_company}
		- Job Title: {job_title}
		- Reason for Call: {call_reason}

		---
		**Call Script Structure**
		1. **Introduction** - Greet the user, introduce yourself and the company.
		2. **Purpose of the Call** - Explain why you are calling.
		3. **Engagement Questions** - Ask relevant questions based on the reason for the call.
		4. **Highlight Key Points** - Summarize key insights or solutions we offer based on the reason for the call.
		5. **Call-to-Action** - Suggest next steps (e.g., scheduling a demo, sending a proposal, etc.).

		**Key Highlights Section:**
		Please tailor this based on the reason for the call: {call_reason}.

		Generate the call script in a professional and engaging manner.
		"""

        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.5}
        )

        if "message" in response and "content" in response["message"]:
            call_script = response["message"]["content"].strip()
            return call_script
        else:
            raise ValueError("Unexpected response format from Ollama.")

    except Exception as e:
        logger.error(f"❌ Error generating call script: {e}", exc_info=True)
        return None


def main():
    """Main function to execute the call script pipeline."""
    logger.info("🚀 Running call script generation pipeline...")

    call_script_formal = generate_call_script(
        "Jack Davis", "Discuss partnership", "TechCorp", "CTO", tone="Formal")
    call_script_casual = generate_call_script(
        "Jack Davis", "Discuss partnership", "TechCorp", "CTO", tone="Casual")
    call_script_persuasive = generate_call_script(
        "Jack Davis", "Discuss partnership", "TechCorp", "CTO", tone="Persuasive")

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
