# Forward Data Lab Project: Education Today

### Professor Profile Extraction Pipeline

My portion of the software system works to uncover and extract useful information about a given professor. I look to capture Research, Biography, Award, & Education information from a select number of professor 'homepages'.

##### `The pipeline can be run independently by executing **\V2\data_main.py**`

#### `Homepage Finding`
- Pulls 3 viable urls to be used for data extraction
- Function located in **\V2 \Homepage_Finding\homepage_finder.py**
- Linked to driver script in **\V2\main.py** which is running the entire process.

#### `Homepage Extraction`
- Modular implementation that scraps a url for text information and classifies different segements of the information.
- **\V2\Homepage_Extraction\homepage_extractor.py** leverages functions from **\V2\Homepage_Extraction\parse_data.py** to scrap and clean html text from beautifulsoup.
- **homepage_extractor.py** uses Random Forest models trained by **random_forest.py** to classify data
- A dictionary with data criterion ('reasearch', 'bio', 'awards', 'education') as values and their associated, classified data packets.

#### `Data Consolidator`
- Currently in infancy stage of development, but aims to merge data packets from all homepage data dictionaries. 
- Implementation currently uses function in **\V2\Data_Consolidator\consolidate_data.py** to merge all information chunks for a given data criteria/value of the homepage data dictionaries
- Plans to improve merging function to achieve better summarization and consolidation.
