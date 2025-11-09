"""Base declarativa compartilhada entre os modelos SQLAlchemy."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
	"""Classe base para os modelos ORM tipados."""

	pass
