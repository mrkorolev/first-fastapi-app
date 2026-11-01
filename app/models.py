from pydantic import BaseModel, Field, field_validator, model_validator

class CalculateRq(BaseModel):
    numbers: list[int] = Field(
        ...,
        description="Список целых чисел для возведения в квадрат",
        examples=[[5, 3, 10]],
    )
    delays: list[float] = Field(
        ...,
        description="Список задержек (в секундах), по одной на каждое число",
        examples=[[1, 2, 0.5]],
    )

    @field_validator("numbers")
    @classmethod
    def validate_numbers(cls, v: list[int]) -> list[int]:
        if not v:
            raise ValueError("numbers не может быть пустым")
        for n in v:
            if n <= 0:
                raise ValueError(f"число должно быть > 0, получено: {n}")
            if n > 10_000:
                raise ValueError(f"число должно быть <= 10000, получено: {n}")
        return v

    @field_validator("delays")
    @classmethod
    def validate_delays(cls, v: list[float]) -> list[float]:
        if not v:
            raise ValueError("delays не может быть пустым")
        for d in v:
            if d <= 0:
                raise ValueError(f"задержка должна быть > 0, получено: {d}")
        return v

    @model_validator(mode="after")
    def check_lengths_match(self) -> CalculateRq:
        if len(self.numbers) != len(self.delays):
            raise ValueError(
                f"длины numbers ({len(self.numbers)}) и delays "
                f"({len(self.delays)}) должны совпадать"
            )
        return self

class Result(BaseModel):
    number: int
    square: int
    delay: float
    time: float

class CalculateRs(BaseModel):
    results: list[Result]
    total_time: float
    parallel_faster_than_sequential: bool