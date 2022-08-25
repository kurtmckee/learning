def display_tokens(tokens, *fields: str):
    """Display tokens. Access tokens are truncated."""

    unique_keys = set(tokens.data.keys()) - {"other_tokens"}
    for token in tokens["other_tokens"]:
        unique_keys -= set(token.keys())

    lengths = []
    for field in fields:
        if field == "access_token":
            lengths.append(10 + 3)
        else:
            length = max(
                [len(field), len(str(tokens[field]))]
                + [len(str(t[field])) for t in tokens["other_tokens"]]
            )
            lengths.append(length)

    print("=" * (sum(lengths) + 10))
    print()
    print(f"{1 + len(tokens['other_tokens'])} tokens received")
    if unique_keys:
        print(f"{len(unique_keys)} unique keys found: {', '.join(unique_keys)}")
    else:
        print("No unique keys found")
    if "refresh_token" in tokens:
        print()
        print("Refresh tokens are present")
    print()
    print()
    print("|".join(f" {field:<{lengths[i]}} " for i, field in enumerate(fields)))
    print("+".join(f"{'-' * (lengths[i] + 2)}" for i in range(len(fields))))
    print(
        "|".join(
            f" {tokens[field]:<{lengths[i]}} "
            if field != "access_token"
            else f" {tokens[field][:10]}... "
            for i, field in enumerate(fields)
        )
    )
    for token in tokens["other_tokens"]:
        print(
            "|".join(
                f" {token[field]:<{lengths[i]}} "
                if field != "access_token"
                else f" {token[field][:10]}... "
                for i, field in enumerate(fields)
            )
        )
    print("+".join(f"{'-' * (lengths[i] + 2)}" for i in range(len(fields))))
    print()
    print()


def revoke_tokens(client, tokens):
    # Revoke tokens.
    for token in [tokens.data, *tokens.data.get("other_tokens", [])]:
        client.oauth2_revoke_token(token["access_token"])
        if "refresh_token" in token:
            client.oauth2_revoke_token(token["refresh_token"])
