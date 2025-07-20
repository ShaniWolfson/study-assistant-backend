# models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # For timestamps
from database import Base  # Use absolute import instead of relative
# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    documents = relationship("Document", back_populates="owner")
    quizzes = relationship("Quiz", back_populates="owner")
    flashcards = relationship("Flashcard", back_populates="owner")
    quiz_attempts = relationship("QuizAttempt", back_populates="owner")

# Document Model
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False) # Raw text content
    summary = Column(Text, nullable=True) # AI-generated summary
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="documents")
    quizzes = relationship("Quiz", back_populates="document")
    flashcards = relationship("Flashcard", back_populates="document")

# Quiz Model
class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    quiz_name = Column(String(255), nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    document = relationship("Document", back_populates="quizzes")
    owner = relationship("User", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz")

# Question Model
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False) # e.g., 'multiple_choice', 'open_ended'
    correct_answer = Column(Text, nullable=True) # For open-ended or just the correct option text for MCQs
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("MCOption", back_populates="question")
    user_answers = relationship("UserAnswer", back_populates="question")

# Multiple Choice Option Model
class MCOption(Base):
    __tablename__ = "mc_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    # Relationships
    question = relationship("Question", back_populates="options")
    user_selections = relationship("UserAnswer", back_populates="selected_option")

# Flashcard Model
class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    term = Column(Text, nullable=False)
    definition = Column(Text, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    document = relationship("Document", back_populates="flashcards")
    owner = relationship("User", back_populates="flashcards")

# Quiz Attempt Model
class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
    score = Column(Integer, nullable=True) # Can be null until graded
    total_questions = Column(Integer, nullable=True)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    user_answers = relationship("UserAnswer", back_populates="attempt")

# User Answer Model
class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    user_selected_option_id = Column(Integer, ForeignKey("mc_options.id"), nullable=True) # For MCQs
    user_open_ended_answer = Column(Text, nullable=True) # For open-ended questions
    is_correct = Column(Boolean, nullable=True) # Can be null until graded
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    attempt = relationship("QuizAttempt", back_populates="user_answers")
    question = relationship("Question", back_populates="user_answers")
    selected_option = relationship("MCOption", back_populates="user_selections")