import yaml
import os


def convert_clash_rules_to_shadowrocket(clash_rules):
    shadowrocket_rules = []
    for rule in clash_rules:
        parts = rule.split(",")
        if len(parts) < 3:
            continue

        rule_type = parts[0].strip()
        rule_value = parts[1].strip()
        rule_policy = parts[2].strip()

        if rule_type == "IP-CIDR":
            shadowrocket_rules.append(f"IP-CIDR,{rule_value},{rule_policy}")
        elif rule_type == "DOMAIN-SUFFIX":
            shadowrocket_rules.append(f"DOMAIN-SUFFIX,{rule_value},{rule_policy}")
        elif rule_type == "RULE-SET":
            # Assuming the rule value is a URL or a file path
            shadowrocket_rules.append(f"RULE-SET,{rule_value},{rule_policy}")
        elif rule_type == "GEOIP":
            shadowrocket_rules.append(f"GEOIP,{rule_value},{rule_policy}")
        elif rule_type == "MATCH":
            shadowrocket_rules.append(f"MATCH,{rule_policy}")
    return shadowrocket_rules


def main():
    file_path = os.path.join(os.path.dirname(__file__), "clash_config_tmp.yaml")
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)

    clash_rules = config.get("rules", [])

    shadowrocket_rules = convert_clash_rules_to_shadowrocket(clash_rules)

    print("[Rule]")
    for rule in shadowrocket_rules:
        print(rule)


if __name__ == "__main__":
    main()
