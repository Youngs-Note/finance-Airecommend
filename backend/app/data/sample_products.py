from backend.app.schemas.product import DataSource, Product, ProductOption, ProductType

SAMPLE_SOURCE_URL = "https://example.com/finance-airecommend/sample-products"


def get_sample_products() -> list[Product]:
    """Return team-authored sample data for local development only."""

    return [
        Product(
            id="sample:deposit:sample-bank-a:deposit-a",
            source=DataSource.SAMPLE,
            source_company_code="sample-bank-a",
            source_product_code="deposit-a",
            product_type=ProductType.DEPOSIT,
            bank_name="샘플 시중은행",
            product_name="샘플 정기예금 A",
            join_way=["인터넷", "스마트폰"],
            join_member="개인",
            special_conditions="온라인 가입 시 샘플 우대금리를 적용합니다.",
            maturity_interest="샘플 데이터이며 실제 상품이 아닙니다.",
            notes="개발용 샘플 데이터",
            max_limit=50_000_000,
            disclosure_month="sample",
            source_url=SAMPLE_SOURCE_URL,
            options=[
                ProductOption(term_months=6, base_rate=2.5, max_rate=2.7, interest_type="단리"),
                ProductOption(
                    term_months=12,
                    base_rate=2.8,
                    max_rate=3.0,
                    interest_type="단리",
                ),
            ],
        ),
        Product(
            id="sample:deposit:sample-bank-b:deposit-b",
            source=DataSource.SAMPLE,
            source_company_code="sample-bank-b",
            source_product_code="deposit-b",
            product_type=ProductType.DEPOSIT,
            bank_name="샘플 시중은행 B",
            product_name="샘플 정기예금 B",
            join_way=["영업점", "인터넷"],
            join_member="개인",
            special_conditions="급여 이체와 카드 실적 조건을 충족하면 샘플 우대금리를 적용합니다.",
            maturity_interest="샘플 데이터이며 실제 상품이 아닙니다.",
            notes="개발용 샘플 데이터",
            max_limit=100_000_000,
            disclosure_month="sample",
            source_url=SAMPLE_SOURCE_URL,
            options=[
                ProductOption(
                    term_months=12,
                    base_rate=2.7,
                    max_rate=3.2,
                    interest_type="단리",
                ),
                ProductOption(
                    term_months=24,
                    base_rate=2.9,
                    max_rate=3.3,
                    interest_type="단리",
                ),
            ],
        ),
        Product(
            id="sample:saving:sample-internet-bank:saving-a",
            source=DataSource.SAMPLE,
            source_company_code="sample-internet-bank",
            source_product_code="saving-a",
            product_type=ProductType.SAVING,
            bank_name="샘플 인터넷전문은행",
            product_name="샘플 자유적금 A",
            join_way=["스마트폰"],
            join_member="개인",
            special_conditions="앱 가입 시 샘플 우대금리를 적용합니다.",
            maturity_interest="샘플 데이터이며 실제 상품이 아닙니다.",
            notes="개발용 샘플 데이터",
            source_url=SAMPLE_SOURCE_URL,
            options=[
                ProductOption(
                    term_months=6,
                    base_rate=3.0,
                    max_rate=3.3,
                    interest_type="단리",
                    saving_type="자유적립식",
                ),
                ProductOption(
                    term_months=12,
                    base_rate=3.2,
                    max_rate=3.6,
                    interest_type="단리",
                    saving_type="자유적립식",
                ),
            ],
        ),
        Product(
            id="sample:saving:sample-bank-a:saving-b",
            source=DataSource.SAMPLE,
            source_company_code="sample-bank-a",
            source_product_code="saving-b",
            product_type=ProductType.SAVING,
            bank_name="샘플 시중은행",
            product_name="샘플 정액적금 B",
            join_way=["영업점", "인터넷", "스마트폰"],
            join_member="개인",
            special_conditions="자동이체와 카드 실적 조건을 충족하면 샘플 우대금리를 적용합니다.",
            maturity_interest="샘플 데이터이며 실제 상품이 아닙니다.",
            notes="개발용 샘플 데이터",
            source_url=SAMPLE_SOURCE_URL,
            options=[
                ProductOption(
                    term_months=12,
                    base_rate=3.1,
                    max_rate=3.8,
                    interest_type="단리",
                    saving_type="정액적립식",
                ),
                ProductOption(
                    term_months=24,
                    base_rate=3.3,
                    max_rate=4.0,
                    interest_type="단리",
                    saving_type="정액적립식",
                ),
            ],
        ),
    ]
