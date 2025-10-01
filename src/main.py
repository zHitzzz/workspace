"""Command line interface for the Google search automation tool."""

from __future__ import annotations

from typing import NoReturn

from google_search import GoogleSearcher, SearchConfig


def main() -> NoReturn:
    """Prompts the user for input and displays Google search results."""

    keyword = input("Nhập từ khóa cần tìm: ").strip()
    if not keyword:
        print("Từ khóa không được để trống.")
        return

    while True:
        total_results_raw = input("Nhập số lượng kết quả muốn xem: ").strip()
        try:
            total_results = int(total_results_raw)
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")
            continue
        if total_results <= 0:
            print("Số lượng kết quả phải lớn hơn 0.")
            continue
        break

    with GoogleSearcher() as searcher:
        search_config = SearchConfig(keyword=keyword, total_results=total_results)
        results = searcher.search(search_config)

    if not results:
        print("Không tìm thấy kết quả phù hợp.")
        return

    for index, result in enumerate(results, start=1):
        print(f"\nKết quả {index}:")
        print(f"Tiêu đề: {result.title}")
        print(f"Mô tả  : {result.description}")


if __name__ == "__main__":
    main()
