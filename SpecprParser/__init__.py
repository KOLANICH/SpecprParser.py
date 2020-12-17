__author__ = "KOLANICH"
__license__ = "Unlicense"

import math
import mmap
import sys
import typing
from io import IOBase
from pathlib import Path

import kaitaistruct
import numpy as np
from kaitaistruct import KaitaiStream

from .kaitai.specpr import Specpr

if not hasattr(math, "inf"):
	math.inf = float("inf")


def reprGenerForAllProps(self):
	return (str(k) + "=" + repr(v) for k, v in self.__dict__.items() if k[0] != "_")


class Record:
	__slots__ = ("ids", "header")

	def __init__(self, krecord: Specpr.Record) -> None:
		self.header = krecord.icflag
		self.ids = None  # to satisfy pylint
		for k, v in krecord.content.__dict__.items():
			if k[0] != "_":
				self.__dict__[k] = v

	@property
	def user(self):
		return self.ids.usernm

	@property
	def title(self):
		return self.ids.ititle

	def __repr__(self):
		return "".join(
			(
				self.__class__.__name__,
				"(",
				", ".join(
					(
						"user=" + repr(self.user),
						"title=" + repr(self.title),
						# ", ".join(repr_generator_for_all_props(self.header))
					)
				),
				")",
			)
		)


class RecordAppendError(NotImplementedError):
	pass


class StartANewRecordError(RecordAppendError):
	def __init__(self):
		super().__init__("Start a new record, this record has already got its metadata")


class InvalidRecordTypeError(RecordAppendError):
	def __init__(self, tp, otherType):
		super().__init__("only " + tp.__name__ + "-compatible are allowed, " + otherType.__name__ + " was passed")


class TextRecord(Record):
	def __init__(self, krecord: Specpr.Record) -> None:
		super().__init__(krecord)
		# self.user=None
		self.chunks = []
		if isinstance(krecord.content, Specpr.TextInitial):
			self.chunks.append(krecord.content.itext)
		else:
			self += krecord

	def __iadd__(self, krecord):
		if isinstance(krecord.content, Specpr.TextContinuation):
			self.chunks.append(krecord.content.tdata)
		elif isinstance(krecord.content, Specpr.TextInitial):
			raise StartANewRecordError()
		else:
			raise InvalidRecordTypeError(Specpr.DataContinuation, type(krecord.content))


class SpectraRecord(Record):
	def __init__(self, krecord: Specpr.Record) -> None:
		super().__init__(krecord)
		if isinstance(krecord.content, Specpr.DataInitial):
			self.data = np.array(self.data)
		else:
			self += krecord

	def __iadd__(self, krecord):
		if isinstance(krecord.content, Specpr.DataContinuation):
			self.data = np.append(self.data, np.array(krecord.content.cdata))
		elif isinstance(krecord.content, Specpr.DataInitial):
			raise StartANewRecordError()
		else:
			raise InvalidRecordTypeError(Specpr.DataContinuation, type(krecord.content))


class SpecprParser:
	__slots__ = ("curParsedRec", "records", "maxRecords")

	def __init__(self, *args, **kwargs) -> None:
		self.records = []
		self.curParsedRec = None
		if args or kwargs:
			self.parse(*args, **kwargs)

	def parse(self, data: Path, maxRecords: typing.Optional[int] = None, skip: int = 1536) -> None:
		"""
		Parses the specpr file.
		the first record of the splib06 library doesn't follow the format, so `skip` skips the first record
		"""
		# pylint:disable=redefined-argument-from-local

		if maxRecords is not None:
			self.maxRecords = maxRecords
		else:
			self.maxRecords = math.inf

		if isinstance(data, Path):
			with data.open("rb") as f:
				self.parse(f, maxRecords=self.maxRecords)
		elif isinstance(data, IOBase):
			with mmap.mmap(data.fileno(), 0, access=mmap.ACCESS_READ) as data:  # causes hang?
				self.parse(data, maxRecords=self.maxRecords)
		else:
			parsed = None
			with KaitaiStream(data) as data:
				data.seek(skip)  # the first record doesn't follow the format.
				parsed = Specpr(data)
			self.preprocess(parsed)

	def appendRecord(self, krecord: Specpr.Record) -> None:
		if krecord.icflag.continuation and self.curParsedRec and self.curParsedRec.header and krecord.icflag.text == self.curParsedRec.header.text:
			self.curParsedRec += krecord
		else:
			recType = TextRecord if krecord.icflag.text else SpectraRecord
			self.curParsedRec = recType(krecord)
			self.records.append(self.curParsedRec)

	def preprocess(self, parsed: Specpr) -> None:
		self.curParsedRec = None
		for krecord in parsed.records:
			self.appendRecord(krecord)
			if len(parsed.records) >= self.maxRecords:
				break
