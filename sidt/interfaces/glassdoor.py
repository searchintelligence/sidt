import requests


class Glassdoor:
    def __init__(self):
        self.headers = {
            "gd-csrf-token": "7-hPL4Z-cJe2BJ8ZeQVAyw:ZsaSPOxNWtrzIXxqaVc02NoMaNF1S3r9B80rC8wvZgZ9oGKPFaY8ipy038pE1W-jZOUsS3u6NwQthBL1HKMiHg:snZOH9Ckc-i2sGtFERtzErtYN0ED7gEVw1-h6zJ6EM0",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }
        self.cookies = {
            'cf_clearance': 'diDfxPspmQmzxwA5uc_xn_1VswfgosDcH8W515oVAhk-1722332150-1.0.1.1-Zza3sLpWsj5fm17qsHfEl1Dg9xB9uosXttgVvRdWgLLUcQe5lnMz8P1Xs.82wTqtvdaKV08CdnQuz03GpqFiLg',
            'gdsid': '1722333229049:1722333229049:76B0E245A728A53EA5A566603046EEA3',
            'asst': '1722333229.0',
            'gdId': '60e35b7b-0803-4943-86aa-6e612f8a9d88',
            'bs': 'tvrxP4dXdwJtVXTvpsl46g:7oMjBnvDqaRjPGfFJnxfGltsEbfvLJEIIoxHFSN0pdSJZeVHlwr29LodOVITqyG1SiS1R79cvPHTZkTd_3MbK-QmgEdjfjqiLwF-pe_thqQ:sdbT1R_a6_1Kqc-vcHXBMN3JBxTvf5Ao79cKyy-LUGY',
            '__cf_bm': 'eUPZdgmXScMPbbse0DqMxjdW_2E7MP_O4eDw1N6y8vc-1722333230-1.0.1.1-nRYEebyFmqDCawvkdqqNimBPU3zLirWpoKMl1uK6LvfUdhZYQl2RzaSlFLzVlAd27iY0rNRY4MTxHrGw3.oAfg',
            '_cfuvid': 'MPBcw8qSRopJypNoWRitXchPDHQM3xZQDwLQvbUvjhw-1722333230252-0.0.1.1-604800000',
            'GSESSIONID': 'undefined',
            'indeedCtk': '1i41gus3uj311801',
            'AWSALB': 'YjsjHZqB5rNz+yKLgmSdX5TUTsB4U0J5RVa5hBmjHZ5wBBBHSVut5bBHeFJM9REzOdnwL9AM2wyYOZnb5DJMIhCLKdtRuGJklwOOqQifpk2Ig4Y/y/bzoSe16cOH',
            'AWSALBCORS': 'YjsjHZqB5rNz+yKLgmSdX5TUTsB4U0J5RVa5hBmjHZ5wBBBHSVut5bBHeFJM9REzOdnwL9AM2wyYOZnb5DJMIhCLKdtRuGJklwOOqQifpk2Ig4Y/y/bzoSe16cOH',
            'JSESSIONID': 'A8080D85D65AFFC227C6049AABF53B40',
            'cass': '0',
        }
    
    def loc_types(self):
        return {
            "N": "COUNTRY",
            "S": "STATE",
            "C": "CITY",
        }
    
    def us_states(self):
        return {
            "Alabama": 105,
            "Alaska": 496,
            "Arizona": 483,
            "Arkansas": 1892,
            "California": 2280,
            "Colorado": 2519,
            "Connecticut": 2697,
            "Delaware": 3523,
            "Florida": 3318,
            "Georgia": 3426,
            "Hawaii": 1385,
            "Idaho": 132,
            "Illinois": 302,
            "Indiana": 2124,
            "Iowa": 2733,
            "Kansas": 3107,
            "Kentucky": 1141,
            "Louisiana": 2792,
            "Maine": 758,
            "Maryland": 3201,
            "Massachusetts": 3399,
            "Michigan": 527,
            "Minnesota": 1775,
            "Mississippi": 1553,
            "Missouri": 386,
            "Montana": 669,
            "Nebraska": 792,
            "Nevada": 2756,
            "New Hampshire": 2403,
            "New Jersey": 39,
            "New Mexico": 1181,
            "New York": 428,
            "North Carolina": 1282,
            "North Dakota": 3517,
            "Ohio": 2235,
            "Oklahoma": 847,
            "Oregon": 3163,
            "Pennsylvania": 3185,
            "Rhode Island": 3156,
            "South Carolina": 3411,
            "South Dakota": 1502,
            "Tennessee": 1968,
            "Texas": 1347,
            "Utah": 255,
            "Vermont": 1765,
            "Virginia": 323,
            "Washington": 3020,
            "West Virginia": 1939,
            "Wisconsin": 481,
            "Wyoming": 1258,
        }

    def get_location(self, query:str):
        # TODO: Fix this somehow, returning 403
        params = {
            "maxLocationsToReturn": "10",
            "term": query,
        }
        response = requests.get(
            "https://www.glassdoor.co.uk/findPopularLocationAjax.htm",
            params=params,
            headers=self.headers,
        )
        return response.text

    def search(self, query:str, loc_id:int, loc_type:str):
        results = []
        cursor = ""
        page = 1

        while True:
            json_data = [
                {
                    "operationName": "JobSearchResultsQuery",
                    "variables": {
                        "keyword": query,
                        "locationId": loc_id,
                        "locationType": loc_type,
                        "numJobsToShow": 100, # Max 100
                        "pageCursor": cursor,
                    },
                    "query": "query JobSearchResultsQuery($excludeJobListingIds: [Long!], $filterParams: [FilterParams], $keyword: String, $locationId: Int, $locationType: LocationTypeEnum, $numJobsToShow: Int!, $originalPageUrl: String, $pageCursor: String, $pageNumber: Int, $pageType: PageTypeEnum, $parameterUrlInput: String, $queryString: String, $seoFriendlyUrlInput: String, $seoUrl: Boolean, $includeIndeedJobAttributes: Boolean) {\n  jobListings(\n    contextHolder: {queryString: $queryString, pageTypeEnum: $pageType, searchParams: {excludeJobListingIds: $excludeJobListingIds, filterParams: $filterParams, keyword: $keyword, locationId: $locationId, locationType: $locationType, numPerPage: $numJobsToShow, pageCursor: $pageCursor, pageNumber: $pageNumber, originalPageUrl: $originalPageUrl, seoFriendlyUrlInput: $seoFriendlyUrlInput, parameterUrlInput: $parameterUrlInput, seoUrl: $seoUrl, searchType: SR, includeIndeedJobAttributes: $includeIndeedJobAttributes}}\n  ) {\n    companyFilterOptions {\n      id\n      shortName\n      __typename\n    }\n    filterOptions\n    indeedCtk\n    jobListings {\n      ...JobView\n      __typename\n    }\n    jobListingSeoLinks {\n      linkItems {\n        position\n        url\n        __typename\n      }\n      __typename\n    }\n    jobSearchTrackingKey\n    jobsPageSeoData {\n      pageMetaDescription\n      pageTitle\n      __typename\n    }\n    paginationCursors {\n      cursor\n      pageNumber\n      __typename\n    }\n    indexablePageForSeo\n    searchResultsMetadata {\n      searchCriteria {\n        implicitLocation {\n          id\n          localizedDisplayName\n          type\n          __typename\n        }\n        keyword\n        location {\n          id\n          shortName\n          localizedShortName\n          localizedDisplayName\n          type\n          __typename\n        }\n        __typename\n      }\n      footerVO {\n        countryMenu {\n          childNavigationLinks {\n            id\n            link\n            textKey\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      helpCenterDomain\n      helpCenterLocale\n      jobAlert {\n        jobAlertId\n        __typename\n      }\n      jobSerpFaq {\n        questions {\n          answer\n          question\n          __typename\n        }\n        __typename\n      }\n      jobSerpJobOutlook {\n        occupation\n        paragraph\n        heading\n        __typename\n      }\n      showMachineReadableJobs\n      __typename\n    }\n    serpSeoLinksVO {\n      relatedJobTitlesResults\n      searchedJobTitle\n      searchedKeyword\n      searchedLocationIdAsString\n      searchedLocationSeoName\n      searchedLocationType\n      topCityIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      topEmployerIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      topEmployerNameResults\n      topOccupationResults\n      __typename\n    }\n    totalJobsCount\n    __typename\n  }\n}\n\nfragment JobView on JobListingSearchResult {\n  jobview {\n    header {\n      indeedJobAttribute {\n        skills\n        extractedJobAttributes {\n          key\n          value\n          __typename\n        }\n        __typename\n      }\n      adOrderId\n      advertiserType\n      ageInDays\n      divisionEmployerName\n      easyApply\n      employer {\n        id\n        name\n        shortName\n        __typename\n      }\n      expired\n      organic\n      employerNameFromSearch\n      goc\n      gocConfidence\n      gocId\n      isSponsoredJob\n      isSponsoredEmployer\n      jobCountryId\n      jobLink\n      jobResultTrackingKey\n      normalizedJobTitle\n      jobTitleText\n      locationName\n      locationType\n      locId\n      needsCommission\n      payCurrency\n      payPeriod\n      payPeriodAdjustedPay {\n        p10\n        p50\n        p90\n        __typename\n      }\n      rating\n      salarySource\n      savedJobId\n      seoJobLink\n      __typename\n    }\n    job {\n      descriptionFragmentsText\n      importConfigId\n      jobTitleId\n      jobTitleText\n      listingId\n      __typename\n    }\n    jobListingAdminDetails {\n      cpcVal\n      importConfigId\n      jobListingId\n      jobSourceId\n      userEligibleForAdminJobDetails\n      __typename\n    }\n    overview {\n      shortName\n      squareLogoUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
                },
            ]

            response = requests.post("https://www.glassdoor.co.uk/graph", headers=self.headers, json=json_data).json()
            
            for result in response[0]["data"]["jobListings"]["jobListings"]:
                results.append({
                    "id": result["jobview"]["job"]["listingId"],
                    "title": result["jobview"]["header"]["jobTitleText"],
                    "location": result["jobview"]["header"]["locationName"],
                    "rating": result["jobview"]["header"]["rating"],
                    "employer": {
                        "name": result["jobview"]["header"]["employer"]["name"],
                        "id": result["jobview"]["header"]["employer"]["id"],
                    },
                })

            cursor_new = None
            for item in response[0]["data"]["jobListings"]["paginationCursors"]:
                if item["pageNumber"] == page + 1:
                    cursor_new = item["cursor"]
                    break
            if cursor_new == None:
                break
            else:
                cursor = cursor_new
                page += 1

        return {
            "expected_result_count": response[0]["data"]["jobListings"]["totalJobsCount"],
            "actual_result_count": len(results),
            "results": results,
        }
