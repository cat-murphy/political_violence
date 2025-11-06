```python
attack_type_list = [
    {
        "attack_type": "FIRE/EXPLOSIVE",
        "definition": "Events where the primary weapon involved was fire, bombs, explosives, an IED, molotov cocktails or other incendiary devices."
    },
    {
        "attack_type": "VEHICLE",
        "definition": "Events where the attack was committed primarily with a vehicle, such as instances of people driving vehicles into crowds."
    },
    {
        "attack_type": "SHOOTING",
        "definition": "Events involving the firing of a firearm. This does not include events of people having but not firing a gun, and it does not include the use of BB guns, pellet guns or airsoft guns."
    },
    {
        "attack_type": "ASSAULT WITH A WEAPON",
        "definition": "Assaults involving the use of a weapon as an instrument of assault, including guns, knives, rods, rocks and other physical objects."
    },
    {
        "attack_type": "ASSAULT",
        "definition": "Events where the primary attack type was physical assault and did not involve a weapon."
    },
    {
        "attack_type": "PROPERTY DESTRUCTION",
        "definition": "Events primarily involving the destruction of property, including buildings, statues and flags."
    }
    {
        "attack_type": "OTHER",
        "definition": "Events that do not involve assault, property destruction, assault with a weapon, fire, explosives, car ramming or shooting."
    }
]

extremist_beliefs_classification_list = [
    {
        "extremist_beliefs_classification": "YES",
        "definition": "Events where the party responsible for initiating the attack has any association with extremist beliefs. This includes Nazism, swastikas, confederate flags, manifestos, ISIS, white power, white nationalism, white supremacy, religious extremism, extremist political groups, militias, conspiracy theories and extreme or genocidal speech. This also includes events involving altercations between two extremist groups, as well as mass shootings and other non-targeted violence against masses of people. It does not include hate crimes not clearly tied to an extremist position. It does not include non-violent political movement organizations."
    },
    {
        "extremist_beliefs_classification": "NO",
        "definition": "Events where the party responsible for initiating the attack is not associated with extremist beliefs of any kind."
    }
]

connection_to_organized_extremist_group_classification_list = [
    {
        "connection_to_organized_extremist_group_classification": "YES",
        "definition": "Events where the party responsible for initiating the violence is a member of an organized extremist group. This includes but is not limited to Patriot Front, militias, violent anarchist groups, violent communist groups, separtists, the Klu Klux Klan, Proud Boys, Groypers, Oath Keepers, Guardian Angels, Rise Above Movement or Boogaloo Boys."
    },
    {
        "connection_to_organized_extremist_group_classification": "NO",
        "definition": "Events where the party responsible for initiating the attack is not a member of an organized extremist group."
    }
]

sole_perpatrator_classification_list = [
    {
        "sole_perpatrator_classification": "YES",
        "definition": "Events where the perpetrator acted alone."
    },
    {
        "sole_perpatrator_classification": "NO",
        "definition": "Events where there were multiple attackers or the number of perpetrators is unclear."
    }
]

issue_type_list = [
    {
        "issue_type": "ISRAEL/PALESTINE",
        "definition": "Events where the primary motive or issue involved in the attack was the conflict in Israel. Key words include Israel, Benjamin Netanyahu, Gaza, Palestine, IDF, occupation, kefiyah, Zionism, genocide, the Oct. 7, 2023, attack or Hamas."
    },
    {
        "issue_type": "COVID",
        "definition": "Events where the primary motive or issue involved in the attack was the COVID-19 pandemic and related policies. Key words include COVID, COVID-19, coronavirus, vaccines, vaccinations, pandemic, masking, social distancing, mask mandates, the slurs 'Chinavirus' or 'Kung Flu' and hydroxychloroquine."
    },
    {
        "issue_type": "REPRODUCTIVE AND WOMEN'S RIGHTS",
        "definition": "Events where the primary motive or issue involved in the attack was reproductive or women's rights, as well as related policies. Key words include reproductive rights, Planned Parenthood, pro-choice, pro-life, abortion and Roe v. Wade."
    },
    {
        "issue_type": "LGBTQ+ RIGHTS",
        "definition": "Events where the primary motive or issue involved in the attack was LGBTQ+ rights and related policies. Key words include drag show, gay and transgender. "
    },
    {
        "issue_type": "IMMIGRATION",
        "definition": "Events where the primary motive or issue involved in the attack was immigration and immigration policy. Key words include immigration, immigrants, ICE, border, migrant and terms related to hate speech such as 'Go back to your country'."
    },
    {
        "issue_type": "BLACK LIVES MATTER",
        "definition": "Events where the primary motive or issue involved in the attack was the Black Lives Matter movement and related topics. Key words include Black Lives Matter, BLM, police brutality, defund, and racial justice."
    },
    {
        "issue_type": "HOMELESSNESS",
        "definition": "Events where the primary motive or issue involved in the attack was homelessness and related policies."
    },
    {
        "issue_type": "OTHER WORLD CONFLICT",
        "definition": "Events where the primary motive or issue involved in the attack was related to world conflicts outside of the conflict in Israel. Key words include Russia, Ukraine, Taiwan, Azerbaijan and Turkish."
    },
    {
        "issue_type": "LABOR",
        "definition": "Events where the primary motive or issue involved in the attack was labor. Key words include labor, workers, strike and collective bargaining."
    },
    {
        "issue_type": "ELECTIONS/VOTING/POLITICS",
        "definition": "Events where the primary motive or issue involved in the attack was related to elections, voting, government institutions or political parties in general but unrelated to already classified issues. Key words include election, ballots, vote, voting, electors, candidate, fradulent, 'Stop the Steal', 'Make America Great Again', 'MAGA', stolen election, election official, poll, council, commissioner, mayor, polling, Republican, Democrat, GOP, Supreme Court, administration, Trump, Biden, Kamala Harris and terms related to specific political figures, officials, agencies, corporations and institutions. "
    },
    {
        "issue_type": "OTHER — CHECK MANUALLY",
        "definition": "Events where a political motive exists but is not one of the already classified issues."
    }
]

target_list = [
    {
        "target": "PUBLIC FIGURE",
        "definition": "Attacks on specific public figures, such as politciians, public officials and cultural figures."
    },
    {
        "target": "INSTITUTION",
        "definition": "Attacks on institutions or political symbols but not specific people, such as attacks on government buildings, agencies, political party offices, statues, churches, mosques, synagogues, police, corporations and organizations.
    },
    {
        "target": "CIVILIANS",
        "definition": "Attacks on civilians in general, including attacks on crowds, random attacks, mass killings and attacks on specific groups of people based on race, identity, religion, gender or ideology.
    }
]

political_violence_classification_list = [
    {
        "political_violence_classification" = "POLITICAL VIOLENCE",
        "definition" = "Events involving violent action against a person, place or institution with a clear political motive."
    },
    {
        "political_violence_classification" = "NOT POLITICAL VIOLENCE",
        "definition" = "Events not involving violence or a clear political motive."
    }
]

I need to build a python script called `classification_script.py`.

Here are the script requirements:
- Use subprocess to call the `llm` command-line tool with the model `claude-4-sonnet` 
- Have the LLM process each event from `us_data_filtered.csv`
- Have the LLM create a `attack_type` field and use the `notes` and `tags` columns to event each story a single attack type from `atack_type_list`. 
- Have the LLM create a `extremist_beliefs_classification` field and assign each event, based on the `notes` and `assoc_actor_1` fields, a yes or no classification from `extremist_beliefs_classification_list` to best describe the beliefs of the perpetrator
- Have the LLM create a `connection_to_organized_extremist_group_classification` field and, for articles where `extremist_beliefs_classification` == 'yes', use `connection_to_organized_extremist_group_classification_list` to assign a yes or no classification to the event.
- Have the LLM create a `issue_type` field and assign each event the single-best fitting issue type based on `issue_type_list`.
- Have the LLM create a `target` field and use `target_list` to classify each event based on the single-best fitting description of the attack's target
- Have the LLM create a `sole_perpatrator_classification` field and use `sole_perpatrator_classification_list` to classify each event based on how many people were responsible for the event.
- Have the LLM create a `political_violence_classification` based on `political_violence_classification_list` to determine whether or not the event qualifies as political violence.
- Have the LLM save the updated events to `us_data_enhanced.json`
- Print progress as it processes events

Here are some guidelines and definitions:
- "Violence" is defined as an event involving a shooting, the use of a weapon, the use of incendiary devices, arson, assault, car ramming or other attack that caused or could reasonably cause bodily harm.
- A "clear political motive" is defined as an explicit tie to a social or inherently political issue, including world conflict, elections, voting, public political figures, political party affiliation, political beliefs, systemic issues, government or social institutions, political symbols, and government actions or policies.
- Mass shootings should be classified as "YES" under `extremist_beliefs_classification` and  "POLITICAL VIOLENCE" under `political_violence_classification`
- "POLITICAL VIOLENCE" includes all events tied to extremist beliefs.
- All events that qualify as hate crimes but are not explicitly tied to a "clear political motive" should be classified as "NOT POLITICAL VIOLENCE".
- "POLITICAL VIOLENCE" includes events where police or military were the target or central issue but not events where police or military initiated the event.
- "PROPERTY DESTRUCTION" is classified as "NOT POLITICAL VIOLENCE" unless the primary weapon was fire or an explosive device and the target was a politically symbolic object.
- There is a hierarchy of `attack_type` classifications. All events involving the use of fire or an incendiary device should be classified as "FIRE/EXPLOSIVE". Events involving the use of vehicles as weapons should be classified as "VEHICLE", unless there was also a shooting. In that case, the `attack_type` should be classified based on which weapon was more likely to harm people. Events involving the discharge of a firearm as well as either assault or the use of another weapon should be classified as "SHOOTING." Events involving physical assault and assault with a weapon should be classified as "ASSAULT WITH A WEAPON."
- The LLM should reference `green_11_5.csv` for classification examples and for guidance on events meeting the criteria for political violence. The LLM should reference `yellow_11_5.csv` for events not meeting the criteria of political violence.
- The LLM should fill fields with "MANUAL CHECK" when it cannot confidently determine the correct classification.
```