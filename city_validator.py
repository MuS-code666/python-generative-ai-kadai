class CityValidator:
    def __init__(self, grid_data):
        """
        コンストラクタ
        :param grid_data: 5x5の高さデータ（リストのリスト）
        """
        self.grid = grid_data
        self.rows = len(grid_data)
        self.cols = len(grid_data[0])

    def check_sunlight(self):
        """
        要件A：日照権チェック
        南側の建物(r+1)が、自分(r)以上の高さの場合、日当たりが悪いと判定。
        :return: 該当する区画の座標リスト [(r, c), ...]
        """
        violations = []

        for row in range(self.rows - 1):
            for col in range(self.cols):
                current_height = self.grid[row][col]
                south_height = self.grid[row + 1][col]

                if current_height == 0 or south_height == 0:
                    continue

                if current_height <= south_height:
                    violations.append((row, col))

        return violations

    def find_crowded_zones(self, threshold):
        """
        要件B：過密エリア特定
        自身＋東西南北の高さ合計がthresholdを超える区画を探す。
        :param threshold: 過密判定の基準値（整数）
        :return: 辞書 {(r, c): total_height, ...}
        """
        crowded_spots = {}

        for row in range(self.rows):
            for col in range(self.cols):
                north_height = self.grid[row - 1][col] if row - 1 >= 0 else 0
                south_height = self.grid[row + 1][col] if row + 1 < self.rows else 0
                west_height = self.grid[row][col - 1] if col - 1 >= 0 else 0
                east_height = self.grid[row][col + 1] if col + 1 < self.cols else 0

                total_height = (
                    self.grid[row][col]
                    + north_height
                    + south_height
                    + west_height
                    + east_height
                )

                if total_height > threshold:
                    crowded_spots[(row, col)] = total_height

        return crowded_spots


# --- 実行・検証用コード（変更不要） ---
if __name__ == "__main__":
    # テストデータ
    test_area = [
        [0, 10, 5, 0, 8],   # 行0
        [0, 12, 6, 0, 8],   # 行1
        [5, 15, 0, 0, 10],  # 行2
        [5, 5,  0, 0, 5],   # 行3
        [0, 0,  0, 0, 0]    # 行4
    ]

    validator = CityValidator(test_area)

    # 1. 日照権チェックの実行
    print("--- 日照権チェック ---")
    sunlight_issues = validator.check_sunlight()
    print(f"日照権侵害リスト: {sunlight_issues}")
    # 期待される出力例: [(0, 1), (1, 2), (2, 4)] など（ロジックに基づいて計算してください）

    # 2. 過密エリアチェックの実行
    print("\n--- 過密エリアチェック (閾値: 30) ---")
    crowded = validator.find_crowded_zones(30)
    print(f"過密エリア: {crowded}")
    # 期待される出力例: {(1, 1): 37, (2, 1): 32} など
