#!/usr/bin/env python3
"""
Classification script for processing political violence events using LLM.
"""

import csv
import json
import subprocess
import sys
from typing import Dict, List, Any
import os

# Classification definitions
ATTACK_TYPE_LIST = [
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
    },
    {
        "attack_type": "OTHER",
        "definition": "Events that do not involve assault, property destruction, assault with a weapon, fire, explosives, car ramming or shooting."
    }
]

EXTREMIST_BELIEFS_CLASSIFICATION_LIST = [
    {
        "extremist_beliefs_classification": "YES",
        "definition": "Events where the party responsible for initiating the attack has any association with extremist beliefs. This includes Nazism, swastikas, confederate flags, manifestos, ISIS, white power, white nationalism, white supremacy, religious extremism, extremist political groups, militias, conspiracy theories and extreme or genocidal speech. This also includes events involving altercations between two extremist groups, as well as mass shootings and other non-targeted violence against masses of people. It does not include hate crimes not clearly tied to an extremist position. It does not include non-violent political movement organizations."
    },
    {
        "extremist_beliefs_classification": "NO",
        "definition": "Events where the party responsible for initiating the attack is not associated with extremist beliefs of any kind."
    }
]

CONNECTION_TO_ORGANIZED_EXTREMIST_GROUP_CLASSIFICATION_LIST = [
    {
        "connection_to_organized_extremist_group_classification": "YES",
        "definition": "Events where the party responsible for initiating the violence is a member of an organized extremist group. This includes but is not limited to Patriot Front, militias, violent anarchist groups, violent communist groups, separtists, the Klu Klux Klan, Proud Boys, Groypers, Oath Keepers, Guardian Angels, Rise Above Movement or Boogaloo Boys."
    },
    {
        "connection_to_organized_extremist_group_classification": "NO",
        "definition": "Events where the party responsible for initiating the attack is not a member of an organized extremist group."
    }
]

SOLE_PERPETRATOR_CLASSIFICATION_LIST = [
    {
        "sole_perpetrator_classification": "YES",
        "definition": "Events where the perpetrator acted alone."
    },
    {
        "sole_perpetrator_classification": "NO",
        "definition": "Events where there were multiple attackers or the number of perpetrators is unclear."
    }
]

ISSUE_TYPE_LIST = [
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
        "definition": "Events where the primary motive or issue involved in the attack was LGBTQ+ rights and related policies. Key words include drag show, gay and transgender."
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
        "definition": "Events where the primary motive or issue involved in the attack was related to elections, voting, government institutions or political parties in general but unrelated to already classified issues. Key words include election, ballots, vote, voting, electors, candidate, fradulent, 'Stop the Steal', 'Make America Great Again', 'MAGA', stolen election, election official, poll, council, commissioner, mayor, polling, Republican, Democrat, GOP, Supreme Court, administration, Trump, Biden, Kamala Harris and terms related to specific political figures, officials, agencies, corporations and institutions."
    },
    {
        "issue_type": "OTHER — CHECK MANUALLY",
        "definition": "Events where a political motive exists but is not one of the already classified issues."
    }
]

TARGET_LIST = [
    {
        "target": "PUBLIC FIGURE",
        "definition": "Attacks on specific public figures, such as politciians, public officials and cultural figures."
    },
    {
        "target": "INSTITUTION",
        "definition": "Attacks on institutions or political symbols but not specific people, such as attacks on government buildings, agencies, political party offices, statues, churches, mosques, synagogues, police, corporations and organizations."
    },
    {
        "target": "CIVILIANS",
        "definition": "Attacks on civilians in general, including attacks on crowds, random attacks, mass killings and attacks on specific groups of people based on race, identity, religion, gender or ideology."
    }
]

POLITICAL_VIOLENCE_CLASSIFICATION_LIST = [
    {
        "political_violence_classification": "POLITICAL VIOLENCE",
        "definition": "Events involving violent action against a person, place or institution with a clear political motive."
    },
    {
        "political_violence_classification": "NOT POLITICAL VIOLENCE",
        "definition": "Events not involving violence or a clear political motive."
    }
]

def load_csv_data(filename: str) -> List[Dict[str, Any]]:
    """Load CSV data into a list of dictionaries."""
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def load_examples() -> tuple:
    """Load example data from green and yellow CSV files."""
    green_examples = []
    yellow_examples = []
    
    try:
        green_examples = load_csv_data('green_11_5.csv')
        print(f"Loaded {len(green_examples)} examples from green_11_5.csv")
    except FileNotFoundError:
        print("Warning: green_11_5.csv not found")
    
    try:
        yellow_examples = load_csv_data('yellow_11_5.csv')
        print(f"Loaded {len(yellow_examples)} examples from yellow_11_5.csv")
    except FileNotFoundError:
        print("Warning: yellow_11_5.csv not found")
    
    return green_examples, yellow_examples

def create_classification_prompt(event: Dict[str, Any], green_examples: List[Dict], yellow_examples: List[Dict]) -> str:
    """Create a prompt for the LLM to classify an event."""
    
    prompt = f"""You are an expert analyst tasked with classifying political violence events. Please analyze the following event and provide classifications based on the criteria below.

EVENT TO CLASSIFY:
Notes: {event.get('notes', '')}
Tags: {event.get('tags', '')}
Associated Actor 1: {event.get('assoc_actor_1', '')}
Actor 1: {event.get('actor1', '')}
Event Type: {event.get('event_type', '')}
Sub Event Type: {event.get('sub_event_type', '')}

CLASSIFICATION CRITERIA:

ATTACK TYPE CLASSIFICATIONS:
{json.dumps(ATTACK_TYPE_LIST, indent=2)}

EXTREMIST BELIEFS CLASSIFICATIONS:
{json.dumps(EXTREMIST_BELIEFS_CLASSIFICATION_LIST, indent=2)}

CONNECTION TO ORGANIZED EXTREMIST GROUP CLASSIFICATIONS:
{json.dumps(CONNECTION_TO_ORGANIZED_EXTREMIST_GROUP_CLASSIFICATION_LIST, indent=2)}

SOLE PERPETRATOR CLASSIFICATIONS:
{json.dumps(SOLE_PERPETRATOR_CLASSIFICATION_LIST, indent=2)}

ISSUE TYPE CLASSIFICATIONS:
{json.dumps(ISSUE_TYPE_LIST, indent=2)}

TARGET CLASSIFICATIONS:
{json.dumps(TARGET_LIST, indent=2)}

POLITICAL VIOLENCE CLASSIFICATIONS:
{json.dumps(POLITICAL_VIOLENCE_CLASSIFICATION_LIST, indent=2)}

GUIDELINES:
- Use the hierarchy for attack_type: FIRE/EXPLOSIVE > VEHICLE > SHOOTING > ASSAULT WITH A WEAPON > ASSAULT > PROPERTY DESTRUCTION > OTHER
- All events involving fire or incendiary devices should be "FIRE/EXPLOSIVE"
- Events with vehicle ramming should be "VEHICLE" unless shooting was primary
- Events with firearm discharge should be "SHOOTING"
- Physical assault with weapons should be "ASSAULT WITH A WEAPON"
- Physical assault without weapons should be "ASSAULT"
- Events primarily involving property destruction should be "PROPERTY DESTRUCTION"
- "Violence" is defined as an event involving a shooting, the use of a weapon, the use of incendiary devices, arson, assault, car ramming or other attack that caused or could reasonably cause bodily harm
- A "clear political motive" is defined as an explicit tie to a social or inherently political issue, including world conflict, elections, voting, public political figures, political party affiliation, political beliefs, systemic issues, government or social institutions, political symbols, and government actions or policies
- Mass shootings should be classified as "YES" under extremist_beliefs_classification and "POLITICAL VIOLENCE" under political_violence_classification
- "POLITICAL VIOLENCE" includes all events tied to extremist beliefs
- All events that qualify as hate crimes but are not explicitly tied to a "clear political motive" should be classified as "NOT POLITICAL VIOLENCE"
- "POLITICAL VIOLENCE" includes events where police or military were the target or central issue but not events where police or military initiated the event
- "PROPERTY DESTRUCTION" is classified as "NOT POLITICAL VIOLENCE" unless the primary weapon was fire or an explosive device and the target was a politically symbolic object
- Use "MANUAL CHECK" if you cannot confidently determine the correct classification

REFERENCE EXAMPLES:
Here are some examples from similar events for reference:

GREEN EXAMPLES (Political Violence):
{json.dumps(green_examples[:3] if green_examples else [], indent=2)}

YELLOW EXAMPLES (Other Events):
{json.dumps(yellow_examples[:3] if yellow_examples else [], indent=2)}

REQUIRED OUTPUT FORMAT:
Please respond with ONLY a valid JSON object containing these seven fields:
{{
    "attack_type": "one of the attack types from the list",
    "extremist_beliefs_classification": "YES or NO",
    "connection_to_organized_extremist_group_classification": "YES, NO, or N/A",
    "sole_perpetrator_classification": "YES or NO",
    "issue_type": "one of the issue types from the list",
    "target": "one of the target types from the list",
    "political_violence_classification": "POLITICAL VIOLENCE or NOT POLITICAL VIOLENCE"
}}

Important: Set connection_to_organized_extremist_group_classification to "N/A" if extremist_beliefs_classification is "NO".
"""
    
    return prompt

def classify_event_with_llm(event: Dict[str, Any], green_examples: List[Dict], yellow_examples: List[Dict]) -> Dict[str, str]:
    """Use LLM to classify a single event."""
    prompt = create_classification_prompt(event, green_examples, yellow_examples)
    
    try:
        # Call the LLM using subprocess
        result = subprocess.run(
            ['/home/codespace/.python/current/bin/llm', '-m', 'claude-4-sonnet', prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"Error calling LLM: {result.stderr}")
            return {
                "attack_type": "MANUAL CHECK",
                "extremist_beliefs_classification": "MANUAL CHECK",
                "connection_to_organized_extremist_group_classification": "MANUAL CHECK",
                "sole_perpetrator_classification": "MANUAL CHECK",
                "issue_type": "MANUAL CHECK",
                "target": "MANUAL CHECK",
                "political_violence_classification": "MANUAL CHECK"
            }
        
        # Parse the JSON response
        response_text = result.stdout.strip()
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_text = response_text[start_idx:end_idx]
                classification = json.loads(json_text)
                
                # Validate the response has required fields
                required_fields = ["attack_type", "extremist_beliefs_classification", "connection_to_organized_extremist_group_classification", "sole_perpetrator_classification", "issue_type", "target", "political_violence_classification"]
                if all(field in classification for field in required_fields):
                    return classification
                else:
                    print(f"Warning: Missing required fields in LLM response")
                    return {
                        "attack_type": "MANUAL CHECK",
                        "extremist_beliefs_classification": "MANUAL CHECK",
                        "connection_to_organized_extremist_group_classification": "MANUAL CHECK",
                        "sole_perpetrator_classification": "MANUAL CHECK",
                        "issue_type": "MANUAL CHECK",
                        "target": "MANUAL CHECK",
                        "political_violence_classification": "MANUAL CHECK"
                    }
            else:
                print(f"Warning: No valid JSON found in LLM response: {response_text[:200]}...")
                return {
                    "attack_type": "MANUAL CHECK",
                    "extremist_beliefs_classification": "MANUAL CHECK",
                    "connection_to_organized_extremist_group_classification": "MANUAL CHECK",
                    "sole_perpetrator_classification": "MANUAL CHECK",
                    "issue_type": "MANUAL CHECK",
                    "target": "MANUAL CHECK",
                    "political_violence_classification": "MANUAL CHECK"
                }
                
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse LLM response as JSON: {e}")
            print(f"Response was: {response_text[:200]}...")
            return {
                "attack_type": "MANUAL CHECK",
                "extremist_beliefs_classification": "MANUAL CHECK",
                "connection_to_organized_extremist_group_classification": "MANUAL CHECK",
                "sole_perpetrator_classification": "MANUAL CHECK",
                "issue_type": "MANUAL CHECK",
                "target": "MANUAL CHECK",
                "political_violence_classification": "MANUAL CHECK"
            }
    
    except subprocess.TimeoutExpired:
        print("Warning: LLM call timed out")
        return {
            "attack_type": "MANUAL CHECK",
            "extremist_beliefs_classification": "MANUAL CHECK",
            "connection_to_organized_extremist_group_classification": "MANUAL CHECK",
            "sole_perpetrator_classification": "MANUAL CHECK",
            "issue_type": "MANUAL CHECK",
            "target": "MANUAL CHECK",
            "political_violence_classification": "MANUAL CHECK"
        }
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return {
            "attack_type": "MANUAL CHECK",
            "extremist_beliefs_classification": "MANUAL CHECK",
            "connection_to_organized_extremist_group_classification": "MANUAL CHECK",
            "sole_perpetrator_classification": "MANUAL CHECK",
            "issue_type": "MANUAL CHECK",
            "target": "MANUAL CHECK",
            "political_violence_classification": "MANUAL CHECK"
        }

def main():
    """Main function to process all events."""
    print("Loading data...")
    
    # Load the main dataset
    try:
        events = load_csv_data('us_data_filtered.csv')
        print(f"Loaded {len(events)} events from us_data_filtered.csv")
    except FileNotFoundError:
        print("Error: us_data_filtered.csv not found")
        sys.exit(1)
    
    # Load example data
    green_examples, yellow_examples = load_examples()
    
    # Process each event
    enhanced_events = []
    total_events = len(events)
    
    print(f"Processing {total_events} events...")
    
    for i, event in enumerate(events, 1):
        print(f"Processing event {i}/{total_events} ({i/total_events*100:.1f}%)")
        
        # Get classification from LLM
        classification = classify_event_with_llm(event, green_examples, yellow_examples)
        
        # Create enhanced event with original data plus new classifications
        enhanced_event = event.copy()
        enhanced_event.update(classification)
        
        enhanced_events.append(enhanced_event)
        
        # Save intermediate results every 50 events
        if i % 50 == 0:
            print(f"Saving intermediate results after {i} events...")
            with open('us_data_enhanced_temp.json', 'w', encoding='utf-8') as f:
                json.dump(enhanced_events, f, indent=2, ensure_ascii=False)
    
    # Save final results
    print("Saving final results to us_data_enhanced.json...")
    with open('us_data_enhanced.json', 'w', encoding='utf-8') as f:
        json.dump(enhanced_events, f, indent=2, ensure_ascii=False)
    
    # Clean up temporary file
    if os.path.exists('us_data_enhanced_temp.json'):
        os.remove('us_data_enhanced_temp.json')
    
    print(f"Classification complete! Processed {total_events} events.")
    
    # Print summary statistics
    attack_types = {}
    extremist_beliefs = {}
    organized_groups = {}
    sole_perpetrators = {}
    issue_types = {}
    targets = {}
    political_violence = {}
    
    for event in enhanced_events:
        attack_type = event.get('attack_type', 'UNKNOWN')
        extremist = event.get('extremist_beliefs_classification', 'UNKNOWN')
        organized = event.get('connection_to_organized_extremist_group_classification', 'UNKNOWN')
        sole_perp = event.get('sole_perpetrator_classification', 'UNKNOWN')
        issue = event.get('issue_type', 'UNKNOWN')
        target = event.get('target', 'UNKNOWN')
        pol_violence = event.get('political_violence_classification', 'UNKNOWN')
        
        attack_types[attack_type] = attack_types.get(attack_type, 0) + 1
        extremist_beliefs[extremist] = extremist_beliefs.get(extremist, 0) + 1
        organized_groups[organized] = organized_groups.get(organized, 0) + 1
        sole_perpetrators[sole_perp] = sole_perpetrators.get(sole_perp, 0) + 1
        issue_types[issue] = issue_types.get(issue, 0) + 1
        targets[target] = targets.get(target, 0) + 1
        political_violence[pol_violence] = political_violence.get(pol_violence, 0) + 1
    
    print("\nSUMMARY STATISTICS:")
    print("Attack Types:")
    for attack_type, count in sorted(attack_types.items()):
        print(f"  {attack_type}: {count}")
    
    print("Extremist Beliefs:")
    for belief, count in sorted(extremist_beliefs.items()):
        print(f"  {belief}: {count}")
    
    print("Organized Group Connection:")
    for connection, count in sorted(organized_groups.items()):
        print(f"  {connection}: {count}")
    
    print("Sole Perpetrator:")
    for sole_perp, count in sorted(sole_perpetrators.items()):
        print(f"  {sole_perp}: {count}")
    
    print("Issue Types:")
    for issue, count in sorted(issue_types.items()):
        print(f"  {issue}: {count}")
    
    print("Targets:")
    for target, count in sorted(targets.items()):
        print(f"  {target}: {count}")
    
    print("Political Violence Classification:")
    for pol_violence, count in sorted(political_violence.items()):
        print(f"  {pol_violence}: {count}")

if __name__ == "__main__":
    main()