import dataclasses

@dataclasses.dataclass
class ResultData:

    # 会社名
    corporate_name: str
    # 採用媒体
    recruit_medium:str
    # 取得日時
    exec_date:str
    # 募集職種
    occupation:str
    # 募集形態
    recruit_form:str
    # 募集URL
    recruit_url:str
    # 勤務地
    working_location:str
    # 募集タイトル
    recruit_title:str
    # 募集詳細
    recruit_detail:str
    # 募集ターゲット
    recruit_target:str
    # 給与
    salary:str
    # キーワード
    keyword:str


    @staticmethod
    def get_field_names():
        """ フィールド名取得
        Returns:
            List: 出力時に使用するフィールド名をリストで定義
        """
        # return ['corporate_name', 'recruit_medium', 'exec_date', 'occupation', 'recruit_form', 'recruit_url', 'working_location', 'recruit_title', 'recruit_detail', 'recruit_target', 'salary', 'keyword']
        return ['会社名', '採用媒体', '取得日時', '募集職種', '募集形態', '募集URL', '勤務地', '募集タイトル', '募集詳細', '募集ターゲット', '給与', 'キーワード']

    def to_list(self):
        """ 配列に変換して返却
        Returns:
            List: 自身の値の配列
        """

        return [self.corporate_name, self.recruit_medium, self.exec_date, self.occupation, self.recruit_form, self.recruit_url, self.working_location, self.recruit_title, self.recruit_detail, self.recruit_target, self.salary, self.keyword]
