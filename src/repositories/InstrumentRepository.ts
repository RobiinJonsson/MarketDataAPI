import { EntityRepository, Repository } from "typeorm";
import { Instrument } from "../entities/Instrument";

@EntityRepository(Instrument)
export class InstrumentRepository extends Repository<Instrument> {
    async findByIdentifier(identifier: string): Promise<Instrument | undefined> {
        return this.createQueryBuilder("instrument")
            .where("instrument.symbol = :identifier", { identifier })
            .orWhere("instrument.isin = :identifier", { identifier })
            .getOne();
    }

    async findWithSchema(identifier: string, schemaAttributes: string[]): Promise<Instrument | undefined> {
        const select = schemaAttributes.map(attr => `instrument.${attr}`);
        return this.createQueryBuilder("instrument")
            .select(select)
            .where("instrument.symbol = :identifier", { identifier })
            .orWhere("instrument.isin = :identifier", { identifier })
            .getOne();
    }
}
