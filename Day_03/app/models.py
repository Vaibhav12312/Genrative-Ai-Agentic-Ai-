
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Record:
    faq_number: str
    category: str
    question: str
    answer: str
    related_form: Optional[str]
    source_url: str

    def __post_init__(self):
        self.faq_number = self.faq_number.strip()
        self.category = self.category.strip()
        self.question = self.question.strip()
        self.answer = self.answer.strip()
        self.source_url = self.source_url.strip()

        if not self.faq_number:
            raise ValueError("FAQ number cannot be empty")

        if not self.category:
            raise ValueError("Category cannot be empty")

        if not self.question:
            raise ValueError("Question cannot be empty")

        if not self.answer:
            raise ValueError("Answer cannot be empty")

        if not self.source_url:
            raise ValueError("Source URL cannot be empty")

        if self.related_form is not None:
            self.related_form = self.related_form.strip() or None

    def to_dict(self):
        return asdict(self)
