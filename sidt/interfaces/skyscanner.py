import requests
import tls_client


class Skyscanner:
    def __init__(self):
        self.api_key = '6f4cb8367f544db99cd1e2ea86fb2627'

    def search(self, origin: str, destination: str, date: str):

        params = {
            'profile': 'minimalmonthviewgridv2',
            'apikey': self.api_key,
        }

        response = requests.get(
            f'https://www.skyscanner.net/g/monthviewservice/UK/GBP/en-GB/calendar/{
                origin}/{destination}/{date}/',
            params=params,
        )

        return response

    def get_cheapest(self, origin: str, destination: str, date: str):
        tls = tls_client.Session(
            client_identifier="chrome128",
            random_tls_extension_order=True
        )
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'cookie': '__Secure-anon_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImM3ZGZlYjI2LTlmZjUtNDY4OC1iYjc3LWRiNTY2NWUyNjFkZSJ9.eyJhenAiOiIyNWM3MGZmZDAwN2JkOGQzODM3NyIsImh0dHBzOi8vc2t5c2Nhbm5lci5uZXQvbG9naW5UeXBlIjoiYW5vbnltb3VzIiwiaHR0cHM6Ly9za3lzY2FubmVyLm5ldC91dGlkIjoiYzZiYjUyNTgtYjIxNC00YzhjLThhOTAtOGU5MDkzM2RiMzQ2IiwiaHR0cHM6Ly9za3lzY2FubmVyLm5ldC9jc3JmIjoiMzEyYjZhODExNDcyOGQzZmE1YTY5MjQ4OGU4YTdiMzYiLCJodHRwczovL3NreXNjYW5uZXIubmV0L2p0aSI6IjAyZjI5Y2FiLThlYjEtNDg5OS05ZTUyLWM0NzgyZjNkY2U2OSIsImlhdCI6MTcxMzg3OTU5MCwiZXhwIjoxNzc2OTUxNTkwLCJhdWQiOiJodHRwczovL2dhdGV3YXkuc2t5c2Nhbm5lci5uZXQvaWRlbnRpdHkiLCJpc3MiOiJodHRwczovL3d3dy5za3lzY2FubmVyLm5ldC9zdHRjL2lkZW50aXR5L2p3a3MvcHJvZC8ifQ.KunT5-lY0yPiPEu_JfhHCXNhtcPae8nIXXC6Mvtp8P7wk5OiLfRbo100JUsfpuPS75odJatW2ax1WpsOllcfSoQx6uEEGD1ROgY0yqg3U11zOK376YBRRlSRs7mKB1m1sHgaoNYAHwuPBtz4Ke-w6oGOl-cPOYbtlPyhj_QiWUi87Aa0c3h6zM35zlOZTU-qAZw2MD1QgV9TIjywdh0lgCjdINqwhmvypizPxFtoPq9CC29-YiVzqpU8dy_jtgXJ_7bY4_8ndfXGYReg0WR5mSgUmLGnI7lCdQLE_AgRixyKEPc_X-YDxxfnOcR4E1ETKgtV97SsFJI7LFZ6r_yvpQ; __Secure-anon_csrf_token=312b6a8114728d3fa5a692488e8a7b36; __Secure-ska=6d0c0e2d-34b4-43f2-9021-fb845f0150bf; _pxhd=ZpRtEcwHUioEZIybeQmivmyueN-7XmyPN5mzIxEUcjUKShTAZf4PcYuhdzuzZz7KbzlRb-U/woATTg6JBE6JVg==:EwuQ0UURO9TEhUxXN5dByvEMkEFVgpdKVWi65Wo8MFsc0ZzxocVBKq5LrsK30ZNSHsSGfRSON1159CqScAcq7SZs9hpvILY8meQ803Q0p4c=; traveller_context=c6bb5258-b214-4c8c-8a90-8e90933db346; abgroup=17274450; ssculture=locale:::en-GB&market:::UK&currency:::GBP; device_guid=6d0c0e2d-34b4-43f2-9021-fb845f0150bf; QSI_S_ZN_0VDsL2Wl8ZAlxlA=v:0:0; pxcts=768ff1b0-8009-11ef-b03f-ef646ea2c388; _pxvid=75b7c9d7-8009-11ef-b3cd-2a5b580284ed; gdpr=information:::true&adverts:::true&tcString:::CQF0FMAQF0FMAGjABBENBJFsAP_gAEPgAAAAJ2NB7CbNLUFC4HpzYKsAMAkHwNBAYoQAAASAAOAFTBKQIIQCgkAQJASgBAACAAIAICZBIQAECAAACEAAQAAAIABEAAAAAAAKIAAAgAAAAAAIAAwCAAAAAAAIgAIAEAAAmAAAAAIAGEAAhAAAAAAAAAAAAAAAAgAAAAAAAAAQAAAIACgAAQJAAAAAAEAAAAAAAAAAAAAAAAAAAAAAABAAQTrgbAALAAeABUADgAIAAZAA0AB4AEQAI4ATAApABVAC6AGIAPQAfgBCACOAE4AKMAYAAwwByQDnAOgAdwA9gB-gEIAIiARYAjgBfQDFAGfAOIAdQA9oCLwFDgKRAWiAvMBfQDBIGTAZOAywBqoD7QH7gP7AhCBN4CdYAAAA.YAAAAAAAAAAA&version:::3; g_state={"i_p":1727950879730,"i_l":2}; preferences=c6bb5258b2144c8c8a908e90933db346; QSI_S_ZN_8fcHUNchqVNRM4S=v:0:0; ssab=Acorn_TCS_Desktop_20_Markets_1_V9:::a&AlternativeDates_V5:::b&Deal_Messaging_Banana_MVP_V2:::b&FalconDummyFeatureExperiment_V1:::b&MAT_car_type_of_grouping_V3:::b&Rail_Cards_Split_Deeplink_V4:::a&SmallerFqsTabsDesktop_V7:::a&WPT_Footer_Flags_OC_Version_V3:::a&append_encrypted_pixel_data_V2:::a&destination_preview_V8:::c&enable_fsc_gc_ocf_month_view_V5:::b&enable_relevant_digital_prebid_V26:::a&exclude_amadeus_calls_V3:::a&footer_iteration_desktop_mvp_V4:::b&footer_oc_upgrade_0_7_18_V3:::a&fps_agora_enabled_version2_V3:::a&fps_agora_superpraas_apply_w_V0:::b&fps_dayview_enable_agora_v2_web_V9:::a&fps_enrichements_desktop_V1:::a&fps_fr_hydra_v3_desktop_V0:::b&fps_new_code_path_desktop_V1:::a&hops_mint_v2_desktop_copy_V1:::a&hotel_ranking_rev_dweb_V4:::a&mat_carhire_ranking_enable_V2:::b&multicity_fsc_gc_V7:::c&mv_hotel_price_V5:::a&price_alerts_runner_test_V7:::b&sam_0837c416b11842e9808832dc3d_V0:::a&sam_0f0129955a3c42dcaabd879725_V0:::b&sam_110f02c37cb74a7f98a08c27e9_V0:::a&sam_177b7079053a407c93bc207515_V0:::a&sam_1826aa8e61144660940eaedb02_V0:::b&sam_2c88cf7b842e49fa86346177f7_V0:::a&sam_2d55480b62af4840aa8f4a6eee_V0:::a&sam_33fe28c72909449a97144a82d5_V0:::a&sam_4254d3078a864c41893dd15ab0_V0:::b&sam_48ad71d58a724b65b6b8ce35fb_V0:::a&sam_531460b56af04c70ab6c74fd6e_V0:::b&sam_544a898ee03c49bdb231fe6443_V0:::b&sam_5467fcc428254b80920853a81e_V0:::a&sam_54f52ee076554da6b0cae3f76a_V0:::b&sam_56eef6d5bb224a779502332f9b_V0:::a&sam_56f43c8176d3472086f5269539_V0:::a&sam_59308f7fc276423aa8d82f83d7_V0:::b&sam_5a0e4d4b9a8e4393b70cd4225e_V0:::b&sam_5b6593509166413587b1161f42_V0:::a&sam_628aae660a5b49f0a30d11be95_V0:::a&sam_656c27b979924768bba70e731a_V0:::a&sam_677c0840a6994a868acd971195_V0:::a&sam_6f879f9551554483afb2ecc209_V0:::b&sam_77389d7c84c44d6db366a6442b_V0:::b&sam_824b7024b07a4479af734f6d8f_V0:::a&sam_92f0fd3cc8104d77835c3e3ff6_V0:::b&sam_9429bd4250854dd3982e6549af_V0:::a&sam_94b3d4c92c564c89a2363dd4ae_V0:::a&sam_a3e96b4c06da4850affb7d2146_V0:::a&sam_a7502351b01a4c50821a2d3072_V0:::a&sam_ac60383b86ae4a17b5ed638b75_V0:::b&sam_b147ff6a4ed14b2e916564ed06_V0:::b&sam_c2c28b789a1e4e848f8f9303d6_V0:::b&sam_c314dc61b8374d969e9edcdd27_V0:::b&sam_cd0ac63374284f69926bd6882c_V0:::a&sam_d1660180420c430694599fe298_V0:::b&sam_d30228426caa4781a90f181dcb_V0:::a&sam_ea1449d016be49fd9377b854c2_V0:::b&sam_fc071253405c4be6befbea785a_V0:::a&sam_fd469aec9acb4088bb1541c7e3_V0:::a&strevda_runtime_GC_wait_slot_V5:::a&strevda_runtime_as_library_V5:::a&terra_proxy_get_v1_entities_V11:::a&terra_proxy_get_v2_entities_V26:::a&terra_proxy_post_v2_search_V8:::a&wordpress_migration_proxy_V15:::a; ssaboverrides=; experiment_allocation_id=cf6264f921d8d256aa621dfc2ec843f14a04ebeb57743fe51d80fa348fd989e0; _px3=a4c38d9a10a6e331fd4688007e5cfe68f0ce1d8cf5ca3b936a7f9ce488f90ac4:yk1QrhTmghbgTaVEMIAPyIUiR8HNij/CL/d8PDu6DxA9NN334IyRCD/SnDHzB2cBY+D1V4Igqok0DkVUFuw5fA==:1000:bOPOWqIDFhMLWUzp1NkIhdKd/KueHS/nzbAXkD2hKieNcgqtuCu7czvwS+L6xpO8rF+1K6JbqAYHMGUwtKhbrdSiVMcG6gsT2LA9pjpxhZRQ8ROh3PaFDoqQ9vDBqpNqjPxlL5hmd5qAN0wmK6By/xvSEf1+5S/QSlQleUkeuAXGbNdzQn8iMMBYXzSOz0xN2YwBhVXThO3SA1v6fpndKCnWbSbUcM8FFqQJKkg8pI8=; jha=AQBSlgcBAAAAAAAAAAAAAAAAZm7+Zkhv/mYA; scanner=currency:::GBP&legs:::UK|2024-10|VGO&tripType:::one-way&rtn:::false&preferDirects:::false&outboundAlts:::false&inboundAlts:::false&oym:::2410&oday&wy:::0&iym:::2410&iday&cabinclass:::Economy&adults:::1&adultsV2:::1&children:::0&childrenV2&infants:::0&from:::UK&to:::VGO',
            'dnt': '1',
            'origin': 'https://www.skyscanner.net',
            'priority': 'u=1, i',
            'referer': 'https://www.skyscanner.net/transport/flights/uk/vgo/?adultsv2=1&cabinclass=economy&childrenv2=&ref=home&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&oym=2410',
            'sec-ch-ua': '"Chromium";v="129", "Not=A?Brand";v="8"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-radar-combined-explore-generic-results': '1',
            'x-radar-combined-explore-unfocused-locations-use-real-data': '1',
            'x-skyscanner-channelid': 'banana',
            'x-skyscanner-combined-results-hotel-polling': 'true',
            'x-skyscanner-combined-results-rail': 'true',
            'x-skyscanner-consent-adverts': 'true',
            'x-skyscanner-currency': 'GBP',
            'x-skyscanner-devicedetection-ismobile': 'false',
            'x-skyscanner-devicedetection-istablet': 'false',
            'x-skyscanner-locale': 'en-GB',
            'x-skyscanner-market': 'UK',
            'x-skyscanner-traveller-context': 'c6bb5258-b214-4c8c-8a90-8e90933db346;1',
            'x-skyscanner-trustedfunnelid': '6c40a021-dc0d-49f2-83d7-823f090ad584',
            'x-skyscanner-utid': 'c6bb5258-b214-4c8c-8a90-8e90933db346',
            'x-skyscanner-viewid': '6c40a021-dc0d-49f2-83d7-823f090ad584',
        }
        json_data = {
            'cabinClass': 'ECONOMY',
            'childAges': [],
            'adults': 1,
            'legs': [
                {
                    'legOrigin': {
                        '@type': 'entity',
                        'entityId': str(origin),
                    },
                    'legDestination': {
                        '@type': 'entity',
                        'entityId': str(destination),
                    },
                    'dates': {
                        '@type': 'month',
                        'year': int(date.split('-')[0]),
                        'month': int(date.split('-')[1]),
                    },
                },
            ],
        }

        response = tls.post(
            'https://www.skyscanner.net/g/radar/api/v2/web-unified-search/',
            headers=headers,
            json=json_data,
        )

        return response
