import { toSnakeCase, toCamelCase } from '../transform';

describe('Case transformation functions', () => {
  describe('toSnakeCase', () => {
    it('should convert camelCase to snake_case', () => {
      const input = {
        keepSpaces: true,
        keepPunctuation: false,
        transformCase: 'keep_case',
        nestedObject: {
          innerCamelCase: true
        }
      };

      const expected = {
        keep_spaces: true,
        keep_punctuation: false,
        transform_case: 'keep_case',
        nested_object: {
          inner_camel_case: true
        }
      };

      expect(toSnakeCase(input)).toEqual(expected);
    });

    it('should handle already snake_case keys', () => {
      const input = {
        already_snake: true,
        another_snake_key: 'value'
      };

      expect(toSnakeCase(input)).toEqual(input);
    });
  });

  describe('toCamelCase', () => {
    it('should convert snake_case to camelCase', () => {
      const input = {
        keep_spaces: true,
        keep_punctuation: false,
        transform_case: 'keep_case',
        nested_object: {
          inner_snake_case: true
        }
      };

      const expected = {
        keepSpaces: true,
        keepPunctuation: false,
        transformCase: 'keep_case',
        nestedObject: {
          innerSnakeCase: true
        }
      };

      expect(toCamelCase(input)).toEqual(expected);
    });

    it('should handle already camelCase keys', () => {
      const input = {
        alreadyCamel: true,
        anotherCamelKey: 'value'
      };

      expect(toCamelCase(input)).toEqual(input);
    });
  });

  describe('Roundtrip conversion', () => {
    it('should maintain data integrity when converting back and forth', () => {
      const original = {
        keepSpaces: true,
        keepPunctuation: false,
        transformCase: 'keep_case'
      };

      const snakeCase = toSnakeCase(original);
      const backToCamel = toCamelCase(snakeCase);

      expect(backToCamel).toEqual(original);
    });
  });
});