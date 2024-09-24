from typing import List

from services.search_result import SearchResult


class PromptCreator:
    def create(self, question: str, documents: List[SearchResult]) -> str:
        general_instructions = self._get_general_instructions()
        model_instructions = self._get_model_instructions()
        question = self._get_question(question)
        search_context = self._get_search_context(documents)

        return self._get_prompt_general_template(general_instructions, model_instructions, question, search_context)

    def _get_prompt_general_template(self, general_instructions: str, model_instructions: str, question: str, search_context: str) -> str:
        return (
            f"{general_instructions} \n"
            f"{model_instructions} \n"
            f"{question} \n"
            f"{search_context}"
        )

    def _get_general_instructions(self) -> str:
        return (
            "Du bist ein erfahrener Kundenservice-Spezialist bei der EV Digital Invest AG. \n"
            "Deine Aufgabe ist es, eine Antwort auf die Frage eines Kunden zu schreiben. \n"
            "Befolge die unten stehenden Anweisungen, um die Frage zu beantworten."
        )

    def _get_model_instructions(self) -> str:
        return (
            "Anweisungen: \n"
            "- Lies die E-Mail des Kunden. Sie befindet sich im Abschnitt \"Frage vom Kunden\". \n"
            "- Fasse die E-Mail zusammen, um eine oder mehrere Fragen des Kunden herauszufiltern, die beantwortet werden müssen.\n"
            "- Analysiere die Suchergebnisse aus der internen Datenbank. Sie befinden sich im Abschnitt \"Suchergebnisse\".\n"
            "- Jedes Suchergebnis steht unter dem Unterabschnitt \"Suchergebnis Nummer x:\", wobei x eine Zahl ab 1 ist.\n"
            "- Jedes Suchergebnis enthält eine \"Antwort\" auf eine \"Frage\".\n"
            "- Wenn das Suchergebnis einen Unterabschnitt \"Anweisungen zur Beantwortung\" enthält, VERWENDE diese Anweisungen.\n"
            "- Denk daran, in Deiner Antwort Links hinzuzufügen, falls im Unterabschnitt \"Anweisungen zur Beantwortung\" ein Link existiert.\n"
            "- VERWENDE keine anderen Informationen, um die Frage des Kunden zu beantworten. VERWENDE nur die Informationen aus dem Abschnitt \"Suchergebnisse\".\n"
            "- Du MUSST deine Antwort als HTML formatieren. Wenn deine Antwort eine Liste von Elementen enthält, formatierst du sie als ungeordnete Liste. \n"
            "- Falls die Frage eine mehrstufige Überlegung erfordert, solltest Du relevante Informationen aus den Suchergebnissen finden und die Antwort auf Grundlage der relevanten Informationen mit logischem Denken zusammenfassen.\n"
            "- Falls die Suchergebnisse keine Informationen enthalten, die die Frage beantworten können, schreibe bitte: \"Ich konnte keine genaue Antwort auf die Frage finden\"."
        )

    def _get_question(self, question: str) -> str:
        return (
            f"Frage vom Kunden: \n"
            f"{question}"
        )

    def _get_search_context(self, documents: List[SearchResult]) -> str:
        search_context = "Suchergebnisse: \n"
        for idx, doc in enumerate(documents):
            formatted_doc = (
                f"Suchergebnis Nummer {idx + 1}: "
                f"Frage: {doc.question}, \n"
                f"Antwort: {doc.answer} \n"
            )

            if doc.answer_instructions is not None:
                formatted_doc += f"Anweisungen zur Beantwortung: {doc.answer_instructions} \n"

            search_context += formatted_doc + " "

        stripped_docs = search_context.strip()

        return stripped_docs
