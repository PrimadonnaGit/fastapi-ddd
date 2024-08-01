# DDD 기반 FastAPI 게시판 프로젝트

이 프로젝트는 Domain-Driven Design (DDD) 원칙을 적용한 FastAPI 기반의 게시판 애플리케이션입니다. SQLModel과 SQLAlchemy를 ORM으로 사용하며, 확장 가능하고 유지보수가
용이한 구조를 갖추고 있습니다.

## 프로젝트 구조

```
src/
└── board/
    ├── domain/
    │   ├── user/
    │   ├── post/
    │   ├── comment/
    │   ├── category/
    │   └── file/
    ├── application/
    │   ├── user/
    │   ├── post/
    │   ├── comment/
    │   ├── category/
    │   └── file/
    ├── infrastructure/
    │   └── persistence/
    │       ├── mappers/
    │       ├── sqlmodel/
    │       └── sqlalchemy/
    └── interfaces/
        └── api/
            └── v1/
├── core/
│   ├── config.py
│   └── di_container.py
└── main.py
```

### 주요 컴포넌트 설명

- `domain/`: 핵심 비즈니스 로직과 엔티티를 포함합니다.
- `application/`: 애플리케이션 서비스와 DTO를 포함합니다.
- `infrastructure/`: 데이터베이스 접근, 외부 서비스 통합 등을 담당합니다.
- `interfaces/`: API 엔드포인트와 같은 외부 인터페이스를 정의합니다.
- `core/`: 애플리케이션 전반의 설정과 의존성 주입 컨테이너를 관리합니다.

## Domain-Driven Design (DDD) 개요

Domain-Driven Design은 복잡한 소프트웨어 프로젝트를 개발할 때 도메인 전문가와 개발자 간의 공통 언어를 사용하여 비즈니스 도메인을 중심으로 설계하는 방법론입니다. DDD는 다음과 같은 핵심 개념과
구성 요소를 가지고 있습니다:

### 1. 유비쿼터스 언어 (Ubiquitous Language)

- 도메인 전문가와 개발자 간의 공통 언어
- 코드, 문서, 대화에서 일관되게 사용

### 2. 한정된 컨텍스트 (Bounded Context)

- 특정 도메인 모델이 적용되는 명확한 경계
- 각 컨텍스트 내에서 모델의 의미가 일관성 있게 유지됨

### 3. 엔티티 (Entity)

- 고유한 식별자를 가진 객체
- 생명주기 동안 계속해서 변경될 수 있음

### 4. 값 객체 (Value Object)

- 속성만으로 식별되는 불변 객체
- 동등성으로 비교됨

### 5. 집합체 (Aggregate)

- 연관된 객체들의 집합
- 하나의 단위로 취급되며, 일관성을 보장

### 6. 도메인 서비스 (Domain Service)

- 특정 엔티티나 값 객체에 속하지 않는 도메인 로직
- 여러 객체 간의 협력이 필요한 연산을 수행

### 7. 리포지토리 (Repository)

- 영속성 저장소에 대한 추상화
- 집합체의 저장 및 검색을 담당

### 8. 응용 서비스 (Application Service)

- 사용자의 요청을 처리
- 도메인 객체들의 협력을 조정

## 이 프로젝트에서의 DDD 적용

이 프로젝트에서는 DDD의 개념을 다음과 같이 적용하였습니다:

1. **도메인 레이어** (`src/board/domain/`):
    - 엔티티, 값 객체, 집합체 정의
    - 도메인 서비스 구현
    - 리포지토리 인터페이스 정의

2. **응용 레이어** (`src/board/application/`):
    - 응용 서비스 구현
    - DTO (Data Transfer Object) 정의

3. **인프라스트럭처 레이어** (`src/board/infrastructure/`):
    - 리포지토리 구현
    - 외부 서비스 통합

4. **인터페이스 레이어** (`src/board/interfaces/`):
    - API 엔드포인트 정의
    - 사용자 인터페이스 (이 프로젝트에서는 API)

5. **유비쿼터스 언어**:
    - 코드, 변수명, 클래스명 등에서 도메인 용어 사용
    - 예: `User`, `Post`, `Comment` 등

6. **한정된 컨텍스트**:
    - 각 도메인 (User, Post, Comment 등)을 별도의 패키지로 구성

7. **의존성 역전 원칙**:
    - 도메인과 응용 계층이 인프라스트럭처에 의존하지 않도록 설계

이러한 DDD 원칙의 적용을 통해, 우리는 다음과 같은 이점을 얻을 수 있습니다:

- 비즈니스 로직의 명확한 표현
- 도메인 전문가와의 효과적인 협업
- 복잡한 비즈니스 규칙의 효과적인 관리
- 유지보수성과 확장성 향상
- 도메인 로직과 기술적 구현의 분리

DDD를 적용함으로써, 이 프로젝트는 단순한 CRUD 애플리케이션을 넘어 복잡한 비즈니스 로직을 효과적으로 표현하고 관리할 수 있는 구조를 가지게 되었습니다.

## DDD를 적용한 이유

1. **비즈니스 로직 중심 설계**: DDD는 비즈니스 도메인에 집중할 수 있게 해줍니다. 이를 통해 기술적 구현보다 비즈니스 요구사항에 더 집중할 수 있습니다.

2. **유연성과 확장성**: 도메인 모델과 인프라스트럭처의 분리를 통해 기술 스택 변경이나 새로운 기능 추가가 용이합니다.

3. **유지보수성 향상**: 명확한 계층 구조와 책임 분리로 인해 코드의 유지보수가 쉬워집니다.

4. **도메인 전문가와의 협업**: 유비쿼터스 언어를 사용함으로써 개발자와 도메인 전문가 간의 소통이 원활해집니다.

5. **테스트 용이성**: 도메인 로직이 독립적이어서 단위 테스트 작성이 쉬워집니다.

## 새로운 도메인 추가 방법

새로운 도메인을 추가할 때는 다음 단계를 따르세요:

1. `domain/` 디렉토리에 새 도메인 폴더 생성 (예: `product/`)
2. 도메인 엔티티, 값 객체, 리포지토리 인터페이스 정의
3. `application/` 디렉토리에 해당 도메인의 서비스와 DTO 구현
4. `infrastructure/persistence/` 에 리포지토리 구현 및 매퍼 추가
5. `interfaces/api/` 에 새 도메인을 위한 API 엔드포인트 추가
6. `core/di_container.py` 에 새 도메인 관련 의존성 주입 설정 추가

예시 (Product 도메인 추가):

```python
# domain/product/product.py
from pydantic import BaseModel


class Product(BaseModel):
    id: Optional[int]
    name: str
    price: float


# domain/product/product_repository.py
from abc import ABC, abstractmethod
from .product import Product


class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product:
        pass


# application/product/product_service.py
class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def create_product(self, name: str, price: float) -> Product:
        product = Product(name=name, price=price)
        return self.product_repository.save(product)


# infrastructure/persistence/sqlmodel/product_repository.py
class SQLModelProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, product: Product) -> Product:
        db_product = ProductModel(**product.dict())
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return Product.from_orm(db_product)


# interfaces/api/v1/product_routes.py
@router.post("/products", response_model=ProductResponseDTO)
def create_product(product: ProductCreateDTO, product_service: ProductService = Depends(get_product_service)):
    return product_service.create_product(product.name, product.price)
```

## 기술 스택

- FastAPI
- SQLModel / SQLAlchemy
- Pydantic
- Dependency Injector

## 설정 및 실행 방법 (Poetry 사용)

이 프로젝트는 의존성 관리와 가상 환경을 위해 Poetry를 사용합니다. 다음 단계를 따라 프로젝트를 설정하고 실행하세요.

1. Poetry 설치 (이미 설치되어 있지 않은 경우):
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. 프로젝트 클론 및 디렉토리 이동:
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

3. Poetry를 사용하여 의존성 설치:
   ```
   poetry install
   ```

4. 가상 환경 활성화:
   ```
   poetry shell
   ```

5. 환경 변수 설정:
   `.env` 파일을 프로젝트 루트 디렉토리에 생성하고 필요한 환경 변수를 설정하세요. 예:
   ```
   DATABASE_URL=sqlite:///./test.db
   SECRET_KEY=your_secret_key_here
   ```

6. 데이터베이스 마이그레이션:
   ```
   poetry run alembic upgrade head
   ```

7. 애플리케이션 실행:
   ```
   poetry run uvicorn src.main:app --reload
   ```