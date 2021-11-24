from transformers import pipeline


class Summary:
    def __init__(self, list_for_summary):
        self.list_for_summary = list_for_summary

    def do_summary(self):
        summarizer = pipeline("summarization")
        text_blocks = self.list_for_summary
        output_list = []
        for block in text_blocks:
            output_list.append(summarizer(block, max_length=50, min_length=5, do_sample=False)[0]["summary_text"])
        return output_list
