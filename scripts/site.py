import sys
import json
import os


def front_matter(d):
    items = "\n".join([f"{k}: {v}" for k, v in d.items()])
    return f"---\n{items}\n---"


def write_index(path, fm):
    with open(f"{path}/_index.md", "w") as fd:
        fd.write(f"{fm}\n\n# Index\n\nA blank index")


def slugify(s):
    return s.lower().strip().replace(" ", "-")


def make_site():
    input = sys.argv[1]
    output = sys.argv[2]

    with open(input) as fd:
        data = json.load(fd)

        soil_types = {st["id"]: st for st in data["soil_types"]}
        soil_criteria = {sc["id"]: sc for sc in data["soil_criteria"]}
        soil_meta = {sm["id"]: sm for sm in data["meta_criteria"]}

    for st in soil_types.values():
        if "Great Group" in st["fields"]:
            st["title"] = st["fields"]["Great Group"]
            st["type"] = "Great Group"
            st["suborder"] = st["fields"]["Suborder"].lower().strip()
            st["order"] = st["fields"]["Order"].lower().strip()
        elif "Suborder" in st["fields"]:
            st["title"] = st["fields"]["Suborder"]
            st["type"] = "Suborder"
            st["order"] = st["fields"]["Order"].lower().strip()
        else:
            st["title"] = st["fields"]["Order"]
            st["type"] = "Order"
        if "Criteria" in st["fields"]:
            criteria_tuples = list(
                zip(st["fields"]["Criteria Types"], st["fields"]["Criteria Names"])
            )
            st["criteria"] = [
                f"[{cn}](/docs/{slugify(ct)}/{slugify(cn)})"
                for ct, cn in criteria_tuples
            ]
        else:
            st["criteria"] = []

        st["slug"] = slugify(st["title"])

    for sc in soil_criteria.values():

        if "Type" in sc["fields"]:
            type_name = sc["fields"]["Type"][0]
            type_slug = slugify(type_name)

            # create taxonomy directory and index, if needed
            try:
                os.makedirs(f"{output}/docs/{type_slug}")
                write_index(
                    f"{output}/docs/{type_slug}",
                    front_matter({"title": type_name, "slug": type_slug}),
                )
            except:
                pass

            sc["slug"] = sc["fields"]["Name"].replace(" ", "-").lower()
            with open(f"{output}/docs/{type_slug}/{sc['slug']}.md", "w") as fd:
                fm = front_matter({"title": sc["fields"]["Name"], "slug": sc["slug"]})
                fd.write(
                    f"""{fm}

**{sc["fields"].get("Summary", "")}**

{sc["fields"].get("Concept", "")}

## Characteristics

{sc["fields"].get("Characteristics", "None found")}

## Horizon Nomenclature

{sc["fields"].get("Horizon Nomenclature", "None found")}

"""
                )

    for st in soil_types.values():
        dir = ""
        name = ""
        breadcrumbs = ""
        if st["type"] == "Order":
            dir = f"{output}/docs/soil-types/{st['slug']}"
            name = "_index.md"
        elif st["type"] == "Suborder":
            dir = f"{output}/docs/soil-types/{st['order']}/{st['slug']}"
            name = "_index.md"
            breadcrumbs = f"[{st['order']}](/docs/soil-types/{st['order']})"
        elif st["type"] == "Great Group":
            dir = f"{output}/docs/soil-types/{st['order']}/{st['suborder']}"
            name = f"{st['slug']}.md"
            breadcrumbs = f"[{st['order']}](/docs/soil-types/{st['order']})"
        os.makedirs(dir, exist_ok=True)

        with open(f"{dir}/{name}", "w") as fd:
            fd.write(
                f"""---
title: {st["fields"]["Name"]}
slug: {st["slug"]}
summary: {st["fields"].get("Summary", "")}
---

{breadcrumbs}

{", ".join(st["criteria"])}

{st["fields"].get("Description", "")}
"""
            )
        # break
    write_index(
        f"{output}/docs/soil-types",
        front_matter({"title": "Soil Types", "slug": "soil-types"}),
    )


if __name__ == "__main__":
    make_site()
