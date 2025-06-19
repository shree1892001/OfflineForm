import json
ai_response = '''{
  "ENTITY NAME": "Punnawalla LLC",
  "DOCUMENT TYPE": "ARTICLES OF ORGANIZATION",
  "ENTITY TYPE": "DOMESTIC LIMITED LIABILITY COMPANY",
  "DOS ID": "7289995",
  "FILE DATE": "03/26/2024",
  "FILE NUMBER": "240326003835",
  "TRANSACTION NUMBER": "202403260004126-3082222",
  "EXISTENCE DATE": "03/26/2024",
  "DURATION/DISSOLUTION": "PERPETUAL",
  "COUNTY ": "KINGS",
  "SERVICE OF PROCESS ADDRESS": "THE LLC 2071 FLATBUSH AVENUE, STE 166, BROOKLYN, NY, 11234, USA",
  "EMAIL": "mayuri@gmail.com",
  "FILLED_BY": "JOHN MOSELEY",
  "FILLER_ADDRESS": "10601 CLARENCE DR. STE. 250, FRISCO, TX, 75033, USA",
  "SIGNATURE": null,  // No signature information available in the text
  "ROLE": null,       // No role information available in the text
  "STATE": "NY"     //  Derived from the address information
}'''
ai_data = json.loads(ai_response)
print(ai_data)