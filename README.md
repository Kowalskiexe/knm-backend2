# Backend dla [strony internetowej Koła Naukowego Matematyków](https://knm.wmi.amu.edu.pl) na UAM

Historia jest taka, że przez liczne wyciecki danych z facebooka, ów portal społecznościowy był tyle razy w sądzie, iż teraz zadbali, aby był trudny do scrapowania.
Dlatego najwygodniej skorzystać z oficjalnego API facebooka, dającego dostęp do postów strony pod warunkiem, że jest się w posiadaniu page access token, który generuje się zgodnie z [dokumentacją](https://developers.facebook.com/docs/facebook-login/guides/access-tokens#pagetokens).

Ten backend właśnie tą metodą pobiera posty z [oficjalnej strony koła na FB](https://www.facebook.com/knm.uam) i udostępnia je w wygodnie dla frontendu formie.

Maciej Kowalski (mackow7@st.amu.edu.pl)
