from spiderNest.action_base import *
import pyperclip


class Action_JiSuMax(BaseAction):
    def __init__(self, silence=True, anti=True, email='@qq.com', life_cycle=61):
        super(Action_JiSuMax, self).__init__(silence, anti, email, life_cycle)

        self.register_url = 'https://jisumax.com/#/register?'

    def sign_up(self, api):
        WebDriverWait(api, 15) \
            .until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='邮箱']"))) \
            .send_keys(self.username)
        for i in api.find_elements_by_xpath("//input[@placeholder='密码']"):
            i.send_keys(self.password)
        api.find_element_by_xpath("//i").click()

    def load_any_subscribe(self, api, element_xpath_str: str, href_xpath_str: str, class_: str):
        time.sleep(1)
        # get trojan link
        api.find_element_by_xpath(
            element_xpath_str).click()

        self.wait(api, 10, 'all')
        api.find_element_by_xpath(href_xpath_str).click()

        self.subscribe = pyperclip.paste()

        save_login_info(self.subscribe, class_, self.life_cycle)

    def run(self):
        api = self.set_spiderOption()
        try:
            api.get(self.register_url)

            self.sign_up(api)

            self.wait(api, 30, "all")

            self.load_any_subscribe(
                api,
                "//a[@class='btn btn-sm btn-primary btn-rounded px-3 mr-1 my-1 ant-dropdown-trigger']",
                "//i[contains(@class,'copy')]",
                'trojan'
            )

            print('trojan:{}'.format(self.subscribe))
        except NoSuchElementException:
            print('jisumax ip is blocked')
        finally:
            api.quit()


if __name__ == '__main__':
    ats = Action_JiSuMax()
    ats.run()
