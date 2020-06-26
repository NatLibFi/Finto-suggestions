export function getTwoEntities(entity: Entity):string {
    console.log(`Will you use ${entity.itemOne} ${entity.itemTwo}`);
    return `Will you use ${entity.itemOne} ${entity.itemTwo}`;
}

interface Entity {
    itemOne: String;
    itemTwo: String;
}