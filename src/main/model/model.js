const util = require("../util");

class Model {
    static get detailsFile() { return "/{}"; }
    static get fields() { return []; }
    static get folder() { return "/"; }
    constructor() {
    }
    static async construct(id) {
        const details = await util.db.getKey(this.detailsFile.replace("{}", id));
        var item = new this();
        this.fields.forEach(field => { item[field] = details[field]; });
        return item;
    }
    toJSON() {
        var details = {};
        this.fields.forEach(field => { details[field] = this[field]; });
        return details;
    }
    async save() {
        if (this.id == undefined) {
            this.id = util.auth.uuid();
        }
        var details = {};
        this.fields.forEach(field => { details[field] = this[field]; });
        await util.db.setKey(this.detailsFile.replace("{}", this.id), details);
        return this.id;
    }
    static async all() {
        const ids = await util.db.listSubKeys(this.folder);
        let items = [];
        for (var id of ids) {
            items.push(await this.construct(id));
        }
        return items;
    }
    static async allJSON() {
        const all = await this.all();
        let json = [];
        for (var item of all) {
            json.push(await item.toJSON());
        }
        return json;
    }
}
exports.Model = Model;
